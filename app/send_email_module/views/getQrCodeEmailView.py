


from typing import Any
from flask.views import View

from markupsafe import escape
from flask import render_template, abort, current_app, session, request, redirect, url_for, flash, jsonify
from ..factory.otp_qr_code_account_message_html import get_otp_qr_code_message_html
from ..factory.emailcontroller import send_simple_email_mime_multipart
from ...two_factor_auth_module.two_fa_auth_controller import load_two_fa_obj

from ...token_module.userTokenModel import UserToken

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
    
    def __init__(self, userToken, UserModel, TwoFaModel, template):
        self.userToken = userToken
        self.twoFaModel = TwoFaModel
        self.userModel = UserModel
        self.template = template
    
    
    def dispatch_request(self, user_token):
        """
        Dispatches the request to handle sending a QR code verification email.

        Returns:
            A redirect response to the appropriate route.
        """
        otp_time_interval = 360
                 
        if request.method == 'GET' and user_token is not None:
            status, token = self.userToken.get_token_by_token(escape(user_token))
            # Check if the token is expired
            if status and self.userToken.is_token_expired(token):
                flash('Token is expired!', 'danger')
                abort(403)
            
            if 'user_id' and 'two_fa_auth_method' and 'firstname' and 'origin_request' and 'lastname' and 'email' in session:
                
                secret = current_app.config['OTP_SECRET_KEY']
                email = session.get('email')
                lastname = session.get('lastname')
                firstname = session.get('firstname')

                if session.get('origin_request') == 'register':
                     
                    # Create an object of the TwoFAModel class             
                    # Call the method with the required data
                    two_fa_obj = load_two_fa_obj({
                        'userID': session.get('user_id'),
                        'two_factor_auth_secret': '',
                        'method_auth': session.get('two_fa_auth_method'),
                        'is_active': True
                    })

                    # Save the secret code in the database
                    respTwoFa, obj = self.twoFaModel.save_two_fa_data(two_fa_obj)                
                elif session.get('origin_request') == 'signin':
                    respTwoFa = True 

                if respTwoFa:
                    
                    otp_qr_code = self.twoFaModel.generate_provisioning_uri(accountname=email, secret=secret)
                    session['otpqrcode'] = otp_qr_code
                    session['otpqrcode_uri'] = 'otp_qrcode_images/' + str(session['otpqrcode'])

                    time_remaining = f"This code expires in 24 hours."

                    flash('Scan the QR Code with your Authenticator Application', 'info')
                    return render_template(self.template, title='2-FA QrCode app', user_token=escape(user_token), otpqrcode_uri=session['otpqrcode_uri'], email=email, time_remaining=time_remaining)
                else:
                    flash('Process failed', 'error')

            else:
                flash('User not identified!', 'danger')         
        

        return redirect(url_for('auth.register'))
            
    