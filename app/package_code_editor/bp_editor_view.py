
import subprocess
from flask import Blueprint, render_template, url_for, redirect, request, session, make_response
from flask_cors import CORS, cross_origin
from markupsafe import escape

bp_editor = Blueprint('laubcode', __name__, url_prefix='/laubcode')
CORS(bp_editor)

@bp_editor.route('/editor')
@cross_origin(methods=['GET'])
def laub_editor():
    user_id = session.get('user_id', None)
    course_id = request.args.get('userID')
    course_content = {}

    response = make_response(render_template('e_learning/code_editor/my_code_editor.html', title="LAUBCode"))
    response.set_cookie('current_page', "course.learn.laubcode") 
    return response


@bp_editor.route('/debug-python')
@cross_origin(methods=['POST'])
def editor_run_python_code():
    code = request.form['code']
    try:
        output = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output
