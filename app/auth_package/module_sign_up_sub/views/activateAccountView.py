import flask
from flask_login import login_user, logout_user
from typing import Any
from flask.views import View

from flask import render_template, session, abort, request, redirect, url_for, flash, jsonify
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
            
            if self.userToken.is_user_token_expired(escape(user_token)):
                abort(401)
            
            #return jsonify({'status': 'success', 'message': self.userToken.is_token_expired(token), 'user_token': escape(user_token)})
            # Get the user details using the email address
            status,token = self.userToken.get_token_by_token(escape(user_token))

            if status and token is not None:
                status, user = self.model.get_user_by_email(token.username)
           
                # Check if the user is identified
                if status and user is not None:
                    
                    # Check if email exists
                    if user.email == token.username:

                        # bEFORE CREATE User generate and save token
                        status, user = self.model.update_user_status(user.userID, True)
                        if status:    
                            logout_user()
                            session.clear()                 
                            return render_template('registered_success.html', user_token=token.token, firstname=user.firstname, lastname=user.lastname, email=user.email)
                        
                        flask.flash('This user is not activated', 'danger')                        
                            
                    else:
                        flash('Invalid user', 'danger') 
                else:
                    flash('Invalid token', 'danger')        
                        
        return render_template(self.template, title='Register')