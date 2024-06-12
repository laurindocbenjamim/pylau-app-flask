import flask
from typing import Any
from flask.views import View

from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, jsonify
from ..controller.userController import load_user_obj, validate_form_fields


class AuthRegisterView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self, model, tokenModel, template):
        self.model = model
        self.template = template
        self.tokenModel = tokenModel

    def dispatch_request(self):
        if request.method == 'POST':

            # Validate form fields
            if validate_form_fields(request.form):                

                # Check if email exists
                if self.model.check_email_exists(request.form.get('email')):
                    flash('Email already exists', 'info')
                
                # Check if phone exists
                elif self.model.check_phone_exists(request.form.get('phone')):
                    flash('Phone already exists', 'info')

                # If email and phone do not exist, create user
                else:

                    # bEFORE CREATE User generate and save token
                    token = self.tokenModel.create_token(request.form.get('email'))
                    if token == False:
                        self.model.db.session.rollback()
                        flash(f'Error creating token {token}', 'error')
                    else:      

                        status,last_user_id = self.model.create_user(load_user_obj(request.form, 'user'))
                        if status:
                            user_token = token.to_dict()['token']
                            
                            two_fa_auth_method = request.form.get('two_fa_auth_method')
                            
                            flask.session['two_fa_auth_method'] = two_fa_auth_method
                            flask.session['user_token'] = token.token
                            flask.session['user_id'] = last_user_id
                            flask.session['firstname'] = request.form.get('firstname')
                            flask.session['lastname'] = request.form.get('lastname')
                            flask.session['email'] = request.form.get('email')
                           
                            if two_fa_auth_method == 'app':
                                #redirectURL = "register/qrcode/generate"
                                flask.flash('The user code has been generated successfully! Please scan the QR code to activate your account.', 'info')                                
                                return redirect(url_for('email.verify_qr_code_send', token=token.token)) 
                            else:
                                #redirectURL = "register/send/opt/email"
                                flask.flash('The user code has been generated successfully! Please check your email to activate your account.', 'info')                                
                                return redirect(url_for('email.verify_code_send', token=token.token))                           
                        else:
                            flash(status, 'error')                    
                        
                        
                    
        return render_template(self.template, title='Register')
