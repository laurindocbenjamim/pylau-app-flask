import flask
from flask_login import login_user, logout_user
from typing import Any
from flask.views import View

from flask import render_template, request, redirect, url_for, flash, jsonify
from markupsafe import escape
from ..controller.userController import load_user_obj, validate_form_fields


class ActivateAccountView(View):
    methods = ['GET']

    def __init__(self, model, userToken, template):
        self.model = model
        self.template = template
        self.userToken = userToken

    def dispatch_request(self, user_token):
        if request.method == 'GET' and user_token is not None:
           
            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status:
                if self.userToken.is_token_expired(token):
                    flash('Token is expired!', 'danger')
                    return redirect(url_for('auth.register'))
            else:
                flash('Token required!', 'danger')
                return redirect(url_for('auth.register'))
            
            
            # Get the user details using the email address
            status, user = self.model.get_user_by_email(token.username)
           
            # Check if the user is identified
            if status and user is not None:
                
                # Check if email exists
                if user.email == token.username:

                    # bEFORE CREATE User generate and save token
                    status, user = self.model.update_user_status(user.userID, True)
                    if status:
                        login_user(user)
                        flask.g.user = user
                        return redirect(url_for('projects.list'))
                    
                    logout_user()
                    flask.flash('This user is not activated', 'danger')                        
                        
                else:
                    flash('Invalid user', 'danger') 
            else:
                flash('Invalid token', 'danger')        
                    
        return render_template(self.template, title='Register')