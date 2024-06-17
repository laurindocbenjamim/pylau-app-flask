from flask import render_template, flash, redirect, url_for, session, jsonify
from flask.views import View
from flask_login import login_user, current_user, logout_user, login_required
from markupsafe import escape

class AdminView(View):
    #decorators = [login_required]
    methods = ['GET']

    def __init__(self, userModel, userToken, template):
        self.userModel = userModel
        self.userToken = userToken
        self.template = template

    def dispatch_request(self, user_token):
            
            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status:
                if self.userToken.is_token_expired(token):
                    flash('Unauthorized authentication!', 'danger')
                    return redirect(url_for('auth.user.login'))
            else:
                flash('Unauthorized authentication!', 'danger')
                return redirect(url_for('auth.user.login'))
            
            # Get the user details using the email address
            status, user = self.userModel.get_user_by_email(token.username)

            # Check if the user is identified

            if status and user is not None:
                
                if user.email == token.username:
                    session['user_token'] = escape(user_token)
                    session['user_id'] = escape(user.userID)
                    session['email'] = escape(user.email)
                   
                    return render_template(self.template, user=user)