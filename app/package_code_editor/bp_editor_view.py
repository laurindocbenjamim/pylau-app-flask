
import subprocess
import ast
import re
from flask import Blueprint, render_template, url_for, redirect, request, session, jsonify, make_response, current_app
from flask_cors import CORS, cross_origin
from .code_editor_factory import CodeEditorFactory

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape
from ..utils import __get_cookies, set_header_params

bp_editor = Blueprint('laubcode', __name__, url_prefix='/laubcode')


# Rate limiter to prevent abuse
#limiter = Limiter(get_remote_address, app=current_app, default_limits = ["1/second"])
#limiter.limit("60/hour")(bp_editor)
#limiter.exempt(doc)

CORS(bp_editor)

# Sanitize input using Python's ast to validate safe code
def sanitize_python_code(code):
    try:
        # Parse the code without executing it
        ast.parse(code)
        return True, ""
    except Exception as e:
        return False, str(e)

def validate_only_string(s):
        # This pattern allows spaces, accentuated characters, and common punctuation
        pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s._-\'"()]+$'
        if re.match(pattern, s):
            return True
        else:
            return False
        
# Use the subprocess library to run any command line
def run_general_command_line(command):
    try:
        output = subprocess.check_output(['python', '-c', command], stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output 


@bp_editor.route('/list-dirs')
@cross_origin(methods=['GET'])
def list_dirs():
    import os
    _DIRECTORY = f'{current_app.config['UPLOAD_FOLDER']}/laubcode'
    dirss = os.listdir(_DIRECTORY)
    return jsonify({"dirs": dirss})

@bp_editor.route('/editor')
@cross_origin(methods=['GET'])
def laub_editor():
    user_id = session.get('user_id', None)
    course_id = request.args.get('userID')
    course_content = {}

    response = make_response(render_template('e_learning/code_editor/my_code_editor.html', title="LAUBCode"))
    #from ..utils.config_headers import set_header_params
    set_header_params(response)
    response.set_cookie('current_page', "course.learn.laubcode") 
    return response



@bp_editor.route('/debug-python',methods=['POST'])

#@cross_origin(methods=['POST'])
def editor_run_python_code():
    code = request.form.get('code', None)
    language = request.form.get('language', None)
    fields = [code, language]

    # Sanitize input
    for field in fields:
        is_safe, error = sanitize_python_code(field)
        if not is_safe:
            #break
            return jsonify({"error": "Invalid Python code: " + error}), 400
    
     
    #return run_general_command_line(code)
    try:
        # Execute the code using subprocess (safer than exec)
        result = subprocess.run(['python3', '-c', code], capture_output=True, text=True, timeout=5)
        if result.stderr:
            return jsonify({"output": result.stderr}), 400
        return jsonify({"output": result.stdout}), 200
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Code execution timed out"}), 400

@bp_editor.route('/root/create-file',  methods=['POST'])
@cross_origin(methods=['POST'])
def create_file():
    status = True
    message = ""
    authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_./"
    
    filename =  request.form.get('filename')
    file_directory =  request.form.get('fileDirectory')
    fields = [file_directory, filename]

    # Validate the entry point
    if any(char not in authorized_chars for char in filename):
        return jsonify({"error": "Invalid characteres for field 'filename'"}), 400
    elif any(char not in authorized_chars for char in file_directory):
        return jsonify({"error": "Invalid characteres: 'file_directory'"}), 400 
    
    # Sanitize input
    for field in fields:
        is_safe, error = sanitize_python_code(field)
        if not is_safe:
            #break
            return jsonify({"error": "Invalid Python code: " + error}), 400

    editor = CodeEditorFactory(f'laubcode/{file_directory}/{str(filename).replace(' ', '')}', 
                               f'laubcode/{file_directory}')
    script = ""
    if '.htm' in filename: script="""<!-- Write your script below -->"""
    elif '.js' in filename or '.css' in filename: script="""/*--Write your script below--*/"""
    elif '.py' in filename: script="""#-- Write your script below --"""
    
    try:
        status, message = editor.create_file(script)
    except Exception as e:
        status=False
        message = str(e)
        
    return jsonify({"status": status, "message": message}, 200)

@bp_editor.route('/save-code/<string:fileName>/<string:fileFormat>', methods=['GET', 'POST'])
#@cross_origin(methods=['GET', 'POST'])
def save_root_script(fileName, fileFormat):
    fileName = escape(fileName)
    fileFormat = escape(fileFormat)
    status = resp = ''
    directory = "laubcode/root"
    directories=[]

    if request.method == 'POST':
        new_script = request.form.get('code')


        is_safe, error = sanitize_python_code(new_script)
        if not is_safe:
            return jsonify({"error": "Invalid Python code: " + error}), 400
        
        editor = CodeEditorFactory(f'{directory}/{str(request.form.get('filename')).replace(' ', '')}', directory)
        #if '.html' in request.form.get('filename'):
        try:
            status, resp = editor.save_file_script(new_script)
        except Exception as e:
            status=False
            resp = str(e)
        
        return jsonify({"status": status, "code": new_script, "directories": directories, "response": resp, "filename": editor.myFILE_PATH}, 200)
    

    filecontent = CodeEditorFactory.read_file(directory,f'{directory}/{fileName}.{fileFormat}')

    return jsonify({"filename": f'{fileName}.{fileFormat}', "directories": directories, "content": filecontent})

@bp_editor.route('/rename-file-name', methods=['POST'])
#@cross_origin(methods=['GET', 'POST'])
def rename_file_name():
    directory = "laubcode/root"
    authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_./"

    old_filename = request.form.get('old_filename')
    new_filename = request.form.get('new_filename')

    # Validate the entry point
    if any(char not in authorized_chars for char in old_filename):
        return jsonify({"error": "Invalid characteres for field 'old_filename'"}), 400
    elif any(char not in authorized_chars for char in new_filename):
        return jsonify({"error": "Invalid characteres: 'new_filename'"}), 400 
    
    fields = [old_filename, new_filename]

    # Sanitize input
    for field in fields:
        is_safe, error = sanitize_python_code(field)
        if not is_safe:
            #break
            return jsonify({"error": "Invalid Python code: " + error}), 400
        
    editor = CodeEditorFactory(f'{directory}/{str(old_filename)}', directory)
    
    try:
        status, resp = editor.rename_file(new_filename.replace(' ', ''))
    except Exception as e:
        status=False
        resp = str(e)
        
    return jsonify({"status": status, "new_filename": new_filename, "response": resp, "filename": editor.myFILE_PATH}, 200)
    
@bp_editor.route('/root/load-scripts')
@cross_origin(methods=['GET'])
def load_root_script():
    
    filename = escape(request.args.get('fileName'))
    editor = CodeEditorFactory(None, None)
    directory = "laubcode/root"
    content_dirs = editor.list_directories("laubcode")

    filelist = editor.load_files(directory=directory)
    
    if not isinstance(filelist, list):
        filelist = ["404", filelist]

    response = make_response(render_template('code_editor/code_editor_simple.html', title="LaubCode", filename=f'{filename}.html', directories=content_dirs, directory=directory, filelist=filelist, USER_DATA=__get_cookies))    
    set_header_params(response)
    return response


@bp_editor.route('/user/load-scripts')
@cross_origin(methods=['GET'])
def load_users_script():
    
    editor = CodeEditorFactory(None, None)

    directory = "laubcode/users"
    filelist = editor.load_files(directory=directory)
    
    if not isinstance(filelist, list):
        filelist = ["404", filelist]

    response = make_response(render_template('code_editor/code_editor_simple.html', title="LaubCode", directory=directory, filelist=filelist, USER_DATA=__get_cookies))    
    set_header_params(response)
    return response




