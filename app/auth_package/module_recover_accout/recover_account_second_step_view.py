
import traceback
import sys
import os
from flask.views import View
from flask import render_template, redirect, url_for, flash, session, jsonify, request
from flask_login import logout_user
from markupsafe import escape
from ...configs_package.modules.logger_config import get_message as set_logger_message

from .recover_account_controller import validate_form_fields

class AccountRecoverSecondStepView(View):
    methods = ['GET', 'POST']

    def __init__(self, userModel, userToken, twoFaModel, template):
        self.userModel = userModel
        self.template = template
        self.userToken = userToken
        self.twoFaModel = twoFaModel

    def dispatch_request(self, user_token):
        userData = {}

        session.pop('_flashes', None)
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

        """
            In this first code we check if the token provide exists
        """
            
        status,token = self.userToken.get_token_by_token(escape(user_token))

            
        if status and token is not None:
            # Get the user details using the email address
            status, user = self.userModel.get_user_by_email(token.username)
            
            # Check if the user is identified
            if status and user is not None:
                new_number = user.phone[7:]
                userData = {
                    "user_id": user.userID,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "username": user.email,
                    "phone": f'*******{new_number}',
                    "token": token.token,
                    "two_fa_auth_method": session['two_fa_auth_method']
                }
            else:
                session.clear()
                logout_user()
                return redirect(url_for('auth.user.login'))
        else:
                session.clear()
                logout_user()
                return redirect(url_for('auth.user.login'))
        
        # If the token exists then the nex step start, by check if it is a POST method requested
        if request.method == 'POST' and user_token is not None:
            
            if validate_form_fields(request.form):
                
                username = request.form.get('username', None)

                try:
                    status, user = self.model.get_user_by_email(username)
                    
                    # First check if the user exists
                    if status and user is not None:
                        
                        # Check if the user has a Token 
                        status, token = self.userToken.get_token_by_user(user.email)
                        
                        if status and token is not None:
                            
                            # Check if the user has two-factor authentication enabled
                            status, two_fa = self.twoFaModel.get_user_two_fa_data(user.userID)
                            
                            if status and two_fa is not None: 
                                if user.is_active() == True:
                                    flash('Your account is already active', 'info')
                                elif user.is_active() == False:
                                    session['username'] = user.email
                                    session['user_token'] = token.token
                                    session['two_fa_auth_method'] = two_fa.method_auth
                                    return redirect(url_for('auth.recover.user_account_st_2',userToken=token.token))     
                            else:
                                flash('2FA Verification failed. Contact the administractor.', 'info') 
                        else:
                                flash('Username not identified', 'danger') 
                    else:
                                flash('Username not found', 'error')                                                 
                            

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    set_logger_message(f"Error occured on [AccountRecoverView]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")                             

        return render_template(self.template, title='Account recovery Step 2', user=userData)
