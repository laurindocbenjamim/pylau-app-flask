import flask
from flask_login import login_user, logout_user
from typing import Any
from flask.views import View

from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from markupsafe import escape
from ..controller.userController import load_user_obj, validate_form_fields


class RemoveUserAccountView(View):
    methods = ['GET']

    def __init__(self, model, userToken):
        self.model = model
        self.userToken = userToken

    def dispatch_request(self, user_id, user_token):
        
        if request.method == 'GET' and user_id is not None and user_token is not None:
            
            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status and token is not None:
                if self.userToken.is_token_expired(token):
                    abort(401)
            else:
                abort(401)
            
            #return jsonify({'status': 'success', 'message': self.userToken.is_token_expired(token), 'user_token': escape(user_token)})
            # Get the user details using the email address
            status, user = self.model.get_user_by_email(token.username)
           
            # Check if the user is identified
            if status and user is not None:
                
                # Check if email exists
                if user.email == token.username:
                    
                    # bEFORE CREATE User generate and save token
                    
                    if self.model.delete_user(escape(user_id)):     
                        flash('User account removed successfully!', 'success')                              
                                                
                    return redirect(url_for('projects.list', user_token=token.token))    
                else:
                    flash('Invalid user', 'danger') 
            else:
                flash('Invalid token', 'danger')        
                    
        return redirect(url_for('index'))