import traceback
import sys
import os
from datetime import datetime, timezone
from flask.views import View

from markupsafe import escape
from flask import request, render_template, abort, session, current_app, redirect, url_for, flash, jsonify
from app.email_module.factory.otp_code_account_message_html import get_otp_code_message_html
from app.email_module.factory.emailcontroller import send_simple_email_mime_multipart
from flask_login import logout_user
from ....configs_package.modules.logger_config import get_message as set_logger_message

class SendAuthCodeEmailView(View):
    """
    This class is responsible for handling the sending of code verification emails to users.

    Methods:
    - dispatch_request(): Handles the GET request for sending the code verification email.
    """

    methods = ['GET']
    
    def __init__(self, userToken, userModel, twoFaModel, template):
        """
        Initializes a new instance of the SendCodeEmailView class.

        Parameters:
        - userModel: An instance of the userModel class.
        - template: The template to be used for rendering the email content.
        """
        self.userToken = userToken
        self.userModel = userModel
        self.twoFaModel = twoFaModel
        self.template = template
    
    def dispatch_request(self, user_token):

        """
            Handles the GET request for sending the code verification email.

            Returns:
            - If the email is sent successfully, redirects to the 2facodeverify endpoint.
            - If the email sending fails, flashes an error message and redirects to the auth.register endpoint.
        """
         
        otp_time_interval = 300
                 
        if request.method == 'GET' and user_token is not None:

            if self.userToken.is_user_token_expired(escape(user_token)):
                session.clear()
                logout_user()
                flash('Your session was expired', 'error')
                return redirect(url_for('auth.user.login'))

            try: 
                status,token = self.userToken.get_token_by_token(escape(user_token))
            
                if status and token is not None:   
                    # Get the user details using the email address
                    status, user = self.userModel.get_user_by_email(token.username)

                    # Check if the user is identified
                    if status and user is not None:
                        
                        if user.email == token.username:
                            secret = current_app.config['OTP_SECRET_KEY']
                            user_id = user.userID
                            email = user.email
                            lastname = user.lastname
                            firstname =user.firstname 
                                
                            totp = self.twoFaModel.generate_otp(accountname=email, secret=secret, interval=otp_time_interval)
                            OTP = totp.now()

                            time_remaining = f"This code expires in {otp_time_interval} seconds ({ int(otp_time_interval / 60) } minutes)"
                            html = get_otp_code_message_html(str(firstname)+" "+str(lastname), OTP, time_remaining)
                            res = send_simple_email_mime_multipart('Code verification', str(email), html, False)

                            if res:
                                flash(f'If the email provided is real, a code to verify your account was sent to <<{email}>>', 'success')
                                return redirect(url_for('auth.user.verify-otp', user_token=escape(user_token)))
                            else:
                                flash('Failed to send code to the email.', 'error')
                        else:
                            flash('Invalid user', 'danger')

                    else:
                        flash('User not identified!', 'danger')         
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                set_logger_message(f"Error occured on [SendAuthCodeEmailView]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")     

        return redirect(url_for('auth.user.login'))
            
    




