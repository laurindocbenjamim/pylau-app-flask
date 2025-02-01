
import traceback
import sys
import os
from flask.views import View
from flask_login import login_user, logout_user
from markupsafe import escape
from flask import render_template, abort, session, request, current_app, g, redirect, url_for, flash, jsonify
from ....configs_package.modules.logger_config import get_message as set_logger_message


class VerifyAuthOtpCodeView(View):
    """
    A class representing a view for verifying OTP codes in a Flask application.

    This view handles the verification of OTP codes entered by the user. It checks if the entered code matches the
    generated OTP code for the user's account. If the verification is successful, a success message is flashed and a
    JSON response is returned. If the verification fails, an error message is flashed.

    Attributes:
        twoFaModel (object): An instance of the two-factor authentication model.
        template (str): The name of the template to be rendered for the view.

    Methods:
        dispatch_request(): Handles the POST request for OTP code verification.

    """

    methods = ['GET', 'POST']
    
    def __init__(self, userToken, userModel, twoFaModel, authUserHistoric, template):
        self.userToken = userToken
        self.userModel = userModel
        self.twoFaModel = twoFaModel
        self.authUserHistoric = authUserHistoric
        self.template = template
    
    def dispatch_request(self, user_token):
        """
        Handles the POST request for OTP code verification.

        This method is called when a POST request is made to the verify OTP code view. It retrieves the entered OTP code
        from the request form and checks if it matches the generated OTP code for the user's account. If the verification
        is successful, a success message is flashed and a JSON response is returned. If the verification fails, an error
        message is flashed.

        Returns:
            If the OTP code verification is successful, a JSON response with a success status and message is returned.
            If the OTP code verification fails, the template for the OTP code verification page is rendered with an
            error message flashed.

        """
        otp_time_interval = 300

                        
        # Check if the token is expired
        if self.userToken.is_user_token_expired(escape(user_token)):
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))
            
        if request.method == 'POST' and user_token is not None:
            
            try:
                status,token = self.userToken.get_token_by_token(escape(user_token))
                        
                
                code = request.form.get('otpcode',None)
                # Get the user details using the email address
                status, user = self.userModel.get_user_by_email(token.username)

                # Check if the user is identified

                if code is not None and status and user is not None:
                    
                    secret = current_app.config['OTP_SECRET_KEY']
                        
                    totp = self.twoFaModel.generate_otp(accountname=user.email, secret=secret, interval=otp_time_interval)
                    otpstatus =  totp.verify(code)
                        
                    if otpstatus:     

                        resp = self.authUserHistoric.create_auth_user(user.userID, user.email, '')
                                        
                        status, user = self.userModel.get_user_by_id(user.userID)
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
                        session['user_token'] = token.token
                            
                        login_user(user)
                        g.user = user  
                        flash('Code verified successful', 'success')
                        return redirect(url_for('index', user_token=str(token.token))) 
                    else:
                        flash('Code verification failed', 'error')
                else:
                    flash(f'User not identified', 'error')
            except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    set_logger_message(f"Error occured on [VerifyAppAuthCodeView]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
        
        return render_template(self.template, title='Code verification', form_title='Enter the code sent to your email', origin='login_auth_email', user_token=escape(user_token))
            
    

    