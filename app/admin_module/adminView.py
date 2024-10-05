from flask import render_template, abort, flash, redirect, url_for, session, jsonify, request, make_response
from flask.views import View
from flask_login import logout_user, login_required
from markupsafe import escape

class AdminView(View):
    decorators = [login_required]
    methods = ['GET']

    def __init__(self, userModel, userToken, template):
        self.userModel = userModel
        self.userToken = userToken
        self.template = template

    def dispatch_request(self, user_token):

        USER_DATA = {
             'USERNAME': request.cookies.get('USERNAME', ''),
        'USER_STATUS': request.cookies.get('USER_STATUS', ''),
        'USER_ROLE': request.cookies.get('USER_ROLE', ''),
        'USER_TOKEN': request.cookies.get('USER_TOKEN', '')
        }
            
        # Check if the token is expired
        """ if self.userToken.is_user_token_expired(escape(user_token)):
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))"""
            
            
        status,token = self.userToken.get_token_by_token(escape(user_token))
            
        if 'user_id' not in session:
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))
            
        # Get the user details using the email address
        status, user = self.userModel.get_user_by_email(token.username)

        # Check if the user is identified

        if not status:
            response = make_response(redirect(url_for('auth.user.logout')))
            from ..utils.config_headers import set_header_params
            set_header_params(response)
            return response
        else:   
            if user.email != token.username:
                response = make_response(redirect(url_for('auth.user.logout')))
                from ..utils.config_headers import set_header_params
                set_header_params(response)
                return response
            else:
                session['user_token'] = token.token
                session['user_id'] = user.userID
                session['email'] = user.email
                response = make_response(render_template(self.template, title="Dashboard", USER_DATA=USER_DATA, user=user, user_token=token.token))
                from ..utils.config_headers import set_header_params
                set_header_params(response)
                response.set_cookie('current_url', request.url)
                return response