

import flask
from typing import Any
from flask.views import View

from flask import render_template, current_app, request, redirect, url_for, flash, jsonify
from ..factory.otp_qr_code_account_message_html import get_otp_qr_code_message_html
from ..factory.emailcontroller import send_simple_email_mime_multipart
from ...two_factor_auth_module.two_fa_auth_controller import load_two_fa_obj



"""
    A class representing a view for sending QR code verification emails in a Flask application.

    This view is responsible for handling GET requests and sending QR code verification emails to users.
    It generates a secret code for the user, saves it in the session, and sends an email with a QR code
    for verification. The email contains the user's first name, last name, and the QR code image.

    Attributes:
        methods (list): A list of HTTP methods allowed for this view (only GET in this case).

    Args:
        model: An instance of the model class used for generating secret codes and saving data.
        template: The template to be rendered for this view.

    Methods:
        dispatch_request(): Handles the GET request and sends the QR code verification email.

    Usage:
        This class should be registered as a view in the Flask application, and the `dispatch_request` method
        should be associated with a URL route.

    Example:
        send_qr_code_view = SendQrCodeEmailView(model=MyModelClass(), template='send_qr_code.html')
        app.add_url_rule('/send_qr_code', view_func=send_qr_code_view.as_view('send_qr_code'))
"""

class GetQrCodeEmailView(View):
    """
    View class for sending a QR code verification email.
    """

    methods = ['GET']
    
    def __init__(self, TwoFaModel, UserModel, template):
        self.twoFaModel = TwoFaModel
        self.userModel = UserModel
        self.template = template
    
    
    def dispatch_request(self, token: str):
        """
        Dispatches the request to handle sending a QR code verification email.

        Returns:
            A redirect response to the appropriate route.
        """
        otp_time_interval = 360
                 
        if request.method == 'GET':
            
            if 'user_id' and 'two_fa_auth_method' and 'firstname'\
                and 'origin_request' and 'lastname' and 'email' in flask.session:

                email = flask.session.get('email')
                lastname = flask.session.get('lastname')
                firstname = flask.session.get('firstname')

                if flask.session.get('origin_request') == 'register':
                    # generate a secret code for the user
                    user_secret_code = self.twoFaModel.generate_secret() 
                    # Create an object of the TwoFAModel class
                    flask.session['two_factor_auth_secret'] = user_secret_code               
                    # Call the method with the required data
                    two_fa_obj = load_two_fa_obj({
                        'userID': flask.session.get('user_id'),
                        'two_factor_auth_secret': user_secret_code,
                        'method_auth': flask.session.get('two_fa_auth_method'),
                        'is_active': True
                    })

                    # Save the secret code in the database
                    respTwoFa, obj = self.twoFaModel.save_two_fa_data(two_fa_obj)                
                elif flask.session.get('origin_request') == 'signin':
                    respTwoFa = True 

                if respTwoFa:
                    #totp = get_otp(obj.two_factor_auth_secret, email , otp_time_interval)
                    secret = secret = current_app.config['OTP_SECRET_KEY']
                    otp_qr_code = self.twoFaModel.generate_provisioning_uri(accountname=email, secret=secret)
                    flask.session['otpqrcode'] = otp_qr_code
                    flask.session['otpqrcode_uri'] = 'otp_qrcode_images/' + str(flask.session['otpqrcode'])

                    time_remaining = f"This code expires in 24 hours."
                    
                    """
                    html = get_otp_qr_code_message_html(str(firstname)+" "+str(lastname), flask.session['otpqrcode_uri'], time_remaining)
                    res = send_simple_email_mime_multipart('Code verification', str(email), html, False)

                    if res:
                        flash(f'If the email provided is real, a Qr code verification was sent to <<{email}>>', 'success')
                        return redirect(url_for('email.2fappqrcodeverify'))
                    else:
                        flash('Email code verification failed', 'error')
                    """
                    flask.flash('Scan the QR Code with your Authenticator Application', 'info')
                    return render_template(self.template, title='2-FA QrCode app', otpqrcode_uri=flask.session['otpqrcode_uri'], email=email, time_remaining=time_remaining)
                else:
                    flash('Process failed', 'error')

            else:
                flash('User not identified!', 'danger')         
        

        return redirect(url_for('auth.register'))
            
    