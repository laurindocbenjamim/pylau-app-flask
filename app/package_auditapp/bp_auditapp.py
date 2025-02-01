
import aiofiles
import os
from quart import Quart, render_template, websocket
from flask_caching import Cache
from flask_cors import CORS, cross_origin
from flask_login import logout_user
from markupsafe import escape
from flask import Blueprint, render_template, redirect, url_for, session, request, make_response, Response

from app.auth_package.module_sign_up_sub.model.users import Users
from app.token_module import UserToken

bp_audit = Blueprint("audit", __name__, url_prefix="/audit")



def read_log_in_chunk(file_path, chunck_size=1024):
    with open(file_path, 'r') as data:
        while True:
            chunck = data.read(chunck_size)
            if not chunck:
                break
            yield chunck

# Generate logs chunck
def generate():
    file_path = "app/static/logs/logs.log"
    if not os.path.exists(file_path):
        yield "=============== File not found =============== "
    else:
        for chunck in read_log_in_chunk(file_path):
            yield chunck

@bp_audit.route('/')
#@cross_origin(methods=['GET'])
def audit():

    if 'user_token' in session:
        user_token = session['user_token']
        if len(escape(user_token)) < 100 or len(escape(user_token)) > 200:
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))            
            
        if UserToken.is_user_token_expired(user_token):
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))
        
        if request.method == 'GET' and user_token is not None:

            status,token = UserToken.get_token_by_token(user_token)
                
            # Get the user details using the email address
            if status and Users.check_email_exists(token.username):
                session['user_token'] = token.token

    resp = make_response(render_template('audit/audit.html', title='Audit App', log='audit/logs'))
    return resp
    
@bp_audit.route('/find', methods=['POST'])
def find():
    text = request.form['text']
    word = request.form['word']
    
    try:
        occurrences = [i for i in range(len(generate())) if text.startswith(word, i)]
        return Response( occurrences, mimetype='text/plain')
    except Exception as e:
        return Response(generate(), mimetype='text/plain')


@bp_audit.route('/goto', methods=['POST'])
def goto():
    text = request.form['text']
    line_number = int(request.form['line'])
    #lines = text.split('\n')
    try:
        text = Response(generate(), mimetype='text/plain')
        lines = text.split('\n')
        if 0 <= line_number < len(lines):
            return Response( lines[line_number], mimetype='text/plain')
            #return jsonify({'line': lines[line_number]})
        #return jsonify({'error': 'Line number out of range'}
        return Response( 'Line number out of range', mimetype='text/plain')
                   
    
        #occurrences = [i for i in range(len(generate())) if text.startswith(word, i)]
        #return Response( occurrences, mimetype='text/plain')
    except Exception as e:
        return Response(f"error {e}", mimetype='text/plain')
                   


@bp_audit.route('/logs')
@cross_origin(methods=['GET'])
#@cache.cached(timeout=60, query_string=True)
def display_logs():

    

    if 'user_token' in session:
        user_token = session['user_token']
        if len(escape(user_token)) < 100 or len(escape(user_token)) > 200:
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))            
            
        if UserToken.is_user_token_expired(user_token):
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))
        
        if request.method == 'GET' and user_token is not None:

            status,token = UserToken.get_token_by_token(user_token)
                
            # Get the user details using the email address
            if status and Users.check_email_exists(token.username):
                session['user_token'] = token.token          

    #return jsonify({"user": session['user_token']})
    logs = "app/static/logs/logs.log"
    
    try:
        return Response(generate(), mimetype='text/plain')
    except Exception as e:
        return Response(generate(), mimetype='text/plain')

    
    
