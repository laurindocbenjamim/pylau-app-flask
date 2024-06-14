
import flask

from flask.views import View

from flask import request, session, current_app, redirect, url_for, flash, jsonify
from ..factory.otp_code_account_message_html import get_otp_code_message_html
from ..factory.emailcontroller import send_simple_email_mime_multipart
from ...two_factor_auth_module.two_fa_auth_controller import load_two_fa_obj



class SendCodeEmailView(View):
    """
    This class is responsible for handling the sending of code verification emails to users.

    Methods:
    - dispatch_request(): Handles the GET request for sending the code verification email.
    """

    methods = ['GET']
    
    def __init__(self, twoFaModel, template):
        """
        Initializes a new instance of the SendCodeEmailView class.

        Parameters:
        - twoFaModel: An instance of the TwoFAModel class.
        - template: The template to be used for rendering the email content.
        """
        self.twoFaModel = twoFaModel
        self.template = template
    
    def dispatch_request(self):

        """
            Handles the GET request for sending the code verification email.

            Returns:
            - If the email is sent successfully, redirects to the 2facodeverify endpoint.
            - If the email sending fails, flashes an error message and redirects to the auth.register endpoint.
        """
         
        otp_time_interval = 300
                 
        if request.method == 'GET':
            
            if 'user_id' and 'two_fa_auth_method' and 'firstname'\
                and 'origin_request' and 'lastname' and 'email' in session:
                secret = current_app.config['OTP_SECRET_KEY']
                user_id = session['user_id']
                email = session.get('email')
                lastname = session.get('lastname')
                firstname = session.get('firstname')
                
                if session.get('origin_request') == 'register':
                    # generate a secret code for the user
                    
                    # Create an object of the TwoFAModel class
                                 
                    # Call the method with the required data
                    two_fa_obj = load_two_fa_obj({
                        'userID': user_id,
                        'two_factor_auth_secret': '',
                        'method_auth': session.get('two_fa_auth_method'),
                        'is_active': True
                    })

                    # Save the secret code in the database
                    respTwoFa, obj = self.twoFaModel.save_two_fa_data(two_fa_obj)                
                elif session.get('origin_request') == 'signin':
                    respTwoFa = True                

                if respTwoFa:
                    
                    totp = self.twoFaModel.generate_otp(accountname=session['email'], secret=secret, interval=otp_time_interval)
                    OTP = totp.now()

                    time_remaining = f"This code expires in {otp_time_interval} seconds ({ int(otp_time_interval / 60) } minutes)"
                    html = get_otp_code_message_html(str(firstname)+" "+str(lastname), OTP, time_remaining)
                    res = send_simple_email_mime_multipart('Code verification', str(email), html, False)

                    if res:
                        #session['user_id'] = user_id
                        #session['email'] = email
                        #session['lastname'] = lastname
                        #session['firstname'] = firstname
                        flash(f'If the email provided is real, a code to verify your account was sent to <<{email}>>', 'success')
                        return redirect(url_for('email.2facodeverify'))
                    else:
                        flash('Email code verification failed', 'error')
                else:
                    flash('Process failed', 'error')

            else:
                flash('User not identified!', 'danger')         
        

        return redirect(url_for('auth.register'))
            
    




