import traceback
import sys
import os
from flask.views import View
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from ..controller.userController import load_user_obj, validate_form_fields
from ....two_factor_auth_module.two_fa_auth_controller import load_two_fa_obj
from ....configs_package.modules.logger_config import get_message as set_logger_message
from app.utils.catch_exception_information import _catch_sys_except_information


class AuthRegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, userToken, twoFaModel, template):
        self.model = model
        self.template = template
        self.userToken = userToken
        self.twoFaModel = twoFaModel

    def dispatch_request(self):
        
        # Check if the user is already logged in
        if 'user_token' in session:
            if session['user_token'] != 'favicon.ico':
                return redirect(url_for('index', user_token=session['user_token']))
        
        
        if request.method == 'POST':
            
            # Validate form fields
            if validate_form_fields(request.form):    
                
                try:
                    
                    # Check if email exists
                    if self.model.check_email_exists(request.form.get('email')):
                        flash('Email already exists', 'info')
                        
                    # Check if phone exists
                    elif self.model.check_phone_exists(request.form.get('phone')):
                        flash('Phone already exists', 'info')

                    # If email and phone do not exist, create user
                    else:
                        
                        # bEFORE CREATE User generate and save token
                        status, token = self.userToken.create_token(request.form.get('email'))
                        
                        if status == False:
                            flash('Error creating token.', 'error')
                        else:      
                            
                            status,last_user_id = self.model.create_user(load_user_obj(form=request.form, role='user'))
                            if status:
                                                        
                                two_fa_auth_method = request.form.get('two_fa_auth_method')
                                
                                session['origin_request'] = 'register'
                                session['two_fa_auth_method'] = two_fa_auth_method
                                session['user_token'] = token.token                            
                                session['user_id'] = last_user_id
                                session['firstname'] = request.form.get('firstname')
                                session['lastname'] = request.form.get('lastname')
                                session['email'] = request.form.get('email')

                                # Create an object of the TwoFAModel class
                                
                                # Call the method with the required data
                                two_fa_obj = load_two_fa_obj({
                                    'userID': last_user_id,
                                    'two_factor_auth_secret': '',
                                    'method_auth': two_fa_auth_method,
                                    'is_active': True
                                })

                                # Save the secret code in the database
                                status, obj = self.twoFaModel.save_two_fa_data(two_fa_obj)
                                
                                if status:
                                    
                                    if two_fa_auth_method == 'app':  
                                        return redirect(url_for('email.2fappqrcodeget', user_token=token.token))                                 
                                    elif two_fa_auth_method == 'email':                               
                                        return redirect(url_for('email.2facodesend', user_token=token.token))  
                                    else:
                                        status, exp_token = self.userToken.force_user_jwt_token_expiration(token.token)
                                        session['user_token'] = exp_token
                                        return redirect(url_for('auth.user.login'))                   
                            else:
                                flash("Failed to create user", 'error')   
                except Exception as e:
                    flash(f'Failed to make login. {type(e).__name__}', 'error')
                    custom_message = "Failed to connect to SMTP. Reconnecting..."
                    error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="send_simple_email", custom_message=custom_message)
                    set_logger_message(error_info)
                        
                    
        return render_template(self.template, title='Register')
    
    