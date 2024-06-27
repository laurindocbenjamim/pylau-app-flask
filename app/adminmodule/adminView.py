from flask import render_template, abort, flash, redirect, url_for, session, jsonify
from flask.views import View
from flask_login import login_user, current_user, logout_user, login_required
from markupsafe import escape

class AdminView(View):
    decorators = [login_required]
    methods = ['GET']

    def __init__(self, userModel, userToken, template):
        self.userModel = userModel
        self.userToken = userToken
        self.template = template

    def dispatch_request(self, user_token):
            
            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status and token is not None:
                if self.userToken.is_token_expired(token):
                    session.clear()
                    logout_user()
                    return redirect(url_for('auth.user.login'))
            else:
                session.clear()
                logout_user()
                return redirect(url_for('auth.user.login'))
            
            if 'user_id' not in session:
                session.clear()
                logout_user()
                return redirect(url_for('auth.user.login'))
            
            # Get the user details using the email address
            status, user = self.userModel.get_user_by_email(token.username)

            # Check if the user is identified

            if status and user is not None:
                
                if user.email == token.username:
                    session['user_token'] = token.token
                    session['user_id'] = user.userID
                    session['email'] = user.email
                   
                    return render_template(self.template, user=user, user_token=token.token)