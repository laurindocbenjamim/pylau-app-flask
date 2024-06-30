
from flask.views import View

from markupsafe import escape
from flask import request, abort, session, current_app, redirect, url_for, flash, jsonify, json
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
            #return jsonify({'status': True, 'token': escape(user_token)})
            #status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            #if status:
                #if self.userToken.is_token_expired(token):
                    #abort(403)
            #else:
                #abort(403)
            if self.userToken.is_user_token_expired(escape(user_token)):
                abort(401)
            
            status,token = self.userToken.get_token_by_token(escape(user_token))
            if status:
                
                # Get the user details using the email address
                status, user = self.userModel.get_user_by_email(token.username)

                
                # Check if the user is identified
                if status and user is not None:
                    
                    
                    secret = current_app.config['OTP_SECRET_KEY']
                    user_id = user.userID
                    email = user.email
                    lastname = user.lastname
                    firstname =user.firstname 
                           
                    totp = self.twoFaModel.generate_otp(accountname=email, secret=secret, interval=otp_time_interval)
                    OTP = totp.now()
                    
                    
                    time_remaining = f"This code expires in 5 minutes)"
                    html = get_otp_code_message_html(str(firstname)+" "+str(lastname), OTP, time_remaining)
                     
                    res = send_simple_email_mime_multipart('Code verification', str(email), html, False)
                    
                    if res:
                        flash(f'If the email provided is real, a code to verify your account was sent to <<{email}>>', 'success')
                        return redirect(url_for('email.2facodeverify', user_token=token.token))
                    else:
                        flash('Failed to send code to the email.', 'error')

                else:
                    flash('User not identified!', 'danger')         
        

        return redirect(url_for('auth.register'))
            
    




