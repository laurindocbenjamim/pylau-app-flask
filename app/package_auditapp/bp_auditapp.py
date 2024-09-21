
from flask_cors import CORS, cross_origin
from flask_login import logout_user
from markupsafe import escape
from flask import Blueprint, render_template, redirect, url_for, session, request, make_response

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


@bp_audit.route('/logs')
@cross_origin(methods=['GET'])
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
    log_data =''
    """with open(logs, 'r') as data:
        log_data = data.read()"""
    log_data = read_log_in_chunk(logs, chunck_size=1024)
    resp = make_response(render_template('home.html', title='Display Logs', log_data=log_data))
    return resp
    
