import traceback
import sys
import os
import flask
from flask_login import login_user, logout_user
from flask.views import View
from flask import render_template, make_response, request, session, redirect, url_for, flash, jsonify,g
from ..controller.authController import validate_form_fields
from ....configs_package.modules.jwt_config import refresh_jwt_token
from ....configs_package.modules.logger_config import get_message as set_logger_message
from app.utils.catch_exception_information import _catch_sys_except_information

class AuthLoginView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, userToken, TwoFaModel, authUserHistoric, template):
        self.model = model
        self.userToken = userToken
        self.TwoFaModel = TwoFaModel
        self.authUserHistoric = authUserHistoric
        self.template = template

    def dispatch_request(self):
        session.pop('_flashes', None)
        recover_account = True

        def finalize_the_login(token, username):            
                     
            status, user = self.model.get_user_by_email(username)
            
            if status:
                session['user_id'] = user.userID
                session['firstname'] = user.firstname
                session['lastname'] = user.lastname
                session['email'] = user.email
                session['country'] = user.country
                session['country_code'] = user.country_code
                session['phone'] = user.phone
                session['active'] = user.active
                session['role'] = user.role
                session['date_added'] = user.date_added
                session['date_updated'] = user.date_updated
                session['user_token'] = token
                                
                login_user(user)
                g.user = user  
                flash('Login success', 'success')
                return redirect(url_for('index', user_token=str(token))) 
            else:
                flask.flash('Login failed. User not found', 'error')
                return redirect(url_for('auth.user.login')) 

        
        # Check if the user is already logged in
        
        if 'user_token' in session:
            
            # Check if the token is expired
            if self.userToken.is_user_token_expired(session['user_token']) == False:
                
                status,token = self.userToken.get_token_by_token(session['user_token'])
                
                # Check if the token is expired
                if status and token:                    
                    if token.is_active==True:
                        return redirect(url_for('index', user_token=token.token))
                    else:
                        session.clear()
                        logout_user()
                else:
                    session.clear()
                    logout_user()
            else:
                session.clear()
                logout_user()
        
        # Check if the user is already logged in
        if request.method == 'POST':
            
            if validate_form_fields(request.form):
                
                username = request.form.get('username')
                password = request.form.get('password')

                try:
                    status, user = self.model.get_user_by_email(username)
                    
                    # First check if the user exists
                    if not status:                        
                        flash('User not found', 'error')
                    else:
                        # Check if the user has a Token 
                        status, u_token = self.userToken.get_token_by_user(user.email)
                        
                        if not status:
                            flash('Something went wrong to check the token', 'error')
                        else:
                            
                            # Check if the user has two-factor authentication enabled
                            status, two_fa = self.TwoFaModel.get_user_two_fa_data(user.userID)
                            
                            if not status:  
                                flash('Something went wrong with (2FA)', 'error')
                            else:     
                                status = user.check_password(password)  
                                           
                                # Check if the user password is correct
                                if not status:
                                    flask.flash('Invalid username or password ', 'error')
                                else:
                                    # Check if the user is activated
                                    
                                    if not user.is_active():
                                        logout_user()                                    
                                        flask.flash(f'This user is not active {user.is_active()}', 'error')
                                    else:
                                        
                                        # generate a secret code for the user
                                        status, new_token = self.userToken.refresh_user_token(u_token.token)                                        
                                        
                                        if not status:
                                            flash("User not  identified", 'error') 
                                        else:                                            
                                            status, up_token = self.userToken.update_token(0,u_token.token, new_token, user.email, False)
                                            
                                            if not status:
                                                flash('Error to update user token', 'error')
                                            else:
                                                # Create an object of the TwoFAModel class
                                                session['user_token'] = new_token                                        
                                                session['two_fa_auth_method'] = two_fa.method_auth
                                                session['origin_request'] = 'signin'
                                                
                                                if two_fa.method_auth == 'app':                                             
                                                    return redirect(url_for('auth.user.app-otp-verify', user_token=new_token))
                                                elif two_fa.method_auth == 'email':
                                                    return redirect(url_for('auth.user.send-otp-email', user_token=new_token))  
                                                else:
                                                    resp = self.authUserHistoric.create_auth_user(user.userID, user.email, '')
                                                    
                                                    status, user = self.model.get_user_by_email(user.email)
            
                                                    if not status:
                                                        flask.flash('Login failed. User not found', 'error')
                                                        return redirect(url_for('auth.user.login')) 
                                                    else:

                                                        
                                                        session['user_id'] = user.userID
                                                        session['firstname'] = user.firstname
                                                        session['lastname'] = user.lastname
                                                        session['email'] = user.email
                                                        session['country'] = user.country
                                                        session['country_code'] = user.country_code
                                                        session['phone'] = user.phone
                                                        session['active'] = user.active
                                                        session['role'] = user.role
                                                        session['date_added'] = user.date_added
                                                        session['date_updated'] = user.date_updated
                                                        session['user_token'] = new_token
                                                                        
                                                        login_user(user)
                                                        g.user = user  
                                                        flash('Login success', 'success')
                                                        return redirect(url_for('index', user_token=str(new_token))) 
                                                        
                                                                                                         
                                                 
                                    
                except Exception as e:
                    flask.flash(f'Failed to make login. {type(e).__name__}', 'error')
                    custom_message = "Failed to connect to SMTP. Reconnecting..."
                    error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="send_simple_email", custom_message=custom_message)
                    set_logger_message(error_info)  

        request.form.get('password', '')

        response = make_response(render_template(self.template, title='Login'))
        return response