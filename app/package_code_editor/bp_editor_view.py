
import subprocess
from flask import Blueprint, render_template, url_for, redirect, request, session, jsonify, make_response, current_app
from flask_cors import CORS, cross_origin
from .code_editor_factory import CodeEditorFactory
from markupsafe import escape
from ..utils import __get_cookies, set_header_params

bp_editor = Blueprint('laubcode', __name__, url_prefix='/laubcode')
CORS(bp_editor)


# Use the subprocess library to run any command line
def run_general_command_line(command):
    try:
        output = subprocess.check_output(['python', '-c', command], stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output 


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


@bp_editor.route('/cont', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def cont():

    if request.method == 'POST':
        return jsonify([{"email": request.form.get('email')}])
    
    return render_template('contact.html', title="CONNTT")



@bp_editor.route('/debug-python',methods=['POST'])
#@cross_origin(methods=['POST'])
def editor_run_python_code():
    code = request.form.get('code', None)
    language = request.form.get('language', None)

     
    return run_general_command_line(code)


@bp_editor.route('/save-code/<string:fileName>/<string:fileFormat>', methods=['GET', 'POST'])
#@cross_origin(methods=['GET', 'POST'])
def save_root_script(fileName, fileFormat):
    fileName = escape(fileName)
    fileFormat = escape(fileFormat)
    status = resp = ''
    directory = "laubcode/root"

    if request.method == 'POST':
        new_script = request.form.get('code')

        editor = CodeEditorFactory(f'{directory}/{str(request.form.get('filename')).replace(' ', '')}', directory)
        #if '.html' in request.form.get('filename'):
        try:
            status, resp = editor.save_html_script(new_script)
        except Exception as e:
            status=False
            resp = str(e)
        
        return jsonify({"status": status, "code": new_script, "response": resp, "filename": editor.myFILE_PATH}, 200)
    

    filecontent = CodeEditorFactory.read_file(directory,f'{directory}/{fileName}.{fileFormat}')

    return jsonify({"filename": f'{fileName}.{fileFormat}', "content": filecontent})

@bp_editor.route('/rename-file-name', methods=['POST'])
#@cross_origin(methods=['GET', 'POST'])
def rename_file_name():
    directory = "laubcode/root"

    old_filename = request.form.get('old_filename')
    new_filename = request.form.get('new_filename')

    editor = CodeEditorFactory(f'{directory}/{str(old_filename)}', directory)
    
    try:
        status, resp = editor.rename_file(new_filename.replace(' ', ''))
    except Exception as e:
        status=False
        resp = str(e)
        
    return jsonify({"status": status, "new_filename": new_filename, "response": resp, "filename": editor.myFILE_PATH}, 200)
    
@bp_editor.route('/root/load-scripts')
def load_root_script():
    

    directory = "laubcode/root"
    filelist = CodeEditorFactory.load_files(directory=directory)
    
    if not isinstance(filelist, list):
        filelist = ["404", filelist]

    response = make_response(render_template('code_editor/code_editor_simple.html', title="LaubCode", directory=directory, filelist=filelist, USER_DATA=__get_cookies))    
    set_header_params(response)
    return response


@bp_editor.route('/user/load-scripts')
def load_users_script():
    

    directory = "laubcode/users"
    filelist = CodeEditorFactory.load_files(directory=directory)
    
    if not isinstance(filelist, list):
        filelist = ["404", filelist]

    response = make_response(render_template('code_editor/code_editor_simple.html', title="LaubCode", directory=directory, filelist=filelist, USER_DATA=__get_cookies))    
    set_header_params(response)
    return response


