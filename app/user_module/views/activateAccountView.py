import flask
from flask_login import login_user, logout_user
from typing import Any
from flask.views import View

from flask import render_template, request, redirect, url_for, flash, jsonify
from markupsafe import escape
from ..controller.userController import load_user_obj, validate_form_fields


class ActivateAccountView(View):
    methods = ['GET']

    def __init__(self, model, tokenModel, template):
        self.model = model
        self.template = template
        self.tokenModel = tokenModel

    def dispatch_request(self, token):
        if request.method == 'GET' and escape(token) is not None:
            token_status,token_obj = self.tokenModel.get_token_by_token(escape(token))
            # Validate token
            if token_status and token_obj.token == escape(token):               
                u_status, user = self.model.get_user_by_email(token_obj.username)
                # Check if email exists
                if u_status and user.email == token_obj.username:

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