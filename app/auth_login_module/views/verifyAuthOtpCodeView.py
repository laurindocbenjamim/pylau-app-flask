

from flask.views import View
from flask_login import login_user, logout_user
from markupsafe import escape
from flask import render_template, session, request, current_app, g, redirect, url_for, flash, jsonify


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
    
    def __init__(self, userToken, userModel, twoFaModel, AuthUserHistoric, template):
        self.userToken = userToken
        self.userModel = userModel
        self.twoFaModel = twoFaModel
        self.AuthUserHistoric = AuthUserHistoric
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

        if request.method == 'GET' and user_token is not None:
            
            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status:
                if self.userToken.is_token_expired(token):
                    flash('Unauthorized authentication!', 'danger')
                    return redirect(url_for('auth.register'))
            else:
                flash('Unauthorized authentication!', 'danger')
                return redirect(url_for('auth.register'))
            
        if request.method == 'POST' and user_token is not None:

            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status:
                if self.userToken.is_token_expired(token):
                    flash('Unauthorized authentication!', 'danger')
                    return redirect(url_for('auth.user.login'))
            else:
                flash('Unauthorized authentication!', 'danger')
                return redirect(url_for('auth.user.login'))
            
            
            code = request.form.get('otpcode',None)
            # Get the user details using the email address
            status, user = self.userModel.get_user_by_email(token.username)

            # Check if the user is identified

            if code is not None and status and user is not None:
                
                if user.email == token.username:
                    secret = current_app.config['OTP_SECRET_KEY']
                    
                    totp = self.twoFaModel.generate_otp(accountname=user.email, secret=secret, interval=otp_time_interval)
                    otpstatus =  totp.verify(code)
                    
                    if otpstatus:     
                        #resp = self.AuthUserHistoric.create_auth_user(user.userID, user.email, '')             
                        session['user_token'] = escape(user_token)
                        user_object = {
                            'user_id': user.userID,
                            'email': user.email,
                            'lastname': user.lastname,
                            'firstname': user.firstname,
                            'active': user.active
                        }
                        flash('Code verified successful', 'success')
                        login_user(user)
                        g.user = user_object
                        return redirect(url_for('index', user_token=escape(user_token))) 
                    else:
                        flash('Code verification failed', 'error')
                else:
                    flash('Invalid user', 'error')
            else:
                flash(f'User not identified', 'error')
        
        return render_template(self.template, title='Code verification', origin='login_auth_email', user_token=escape(user_token))
            
    

    