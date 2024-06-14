
import flask
from flask.views import View
from flask_login import login_user, logout_user

from flask import render_template, request, current_app, g, redirect, url_for, flash, jsonify



class VerifyOtpCodeView(View):
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
    
    def __init__(self, twoFaModel, UserModel, template):
        self.twoFaModel = twoFaModel
        self.UserModel = UserModel
        self.template = template
    
    def dispatch_request(self):
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
                 
        if request.method == 'POST':
            code = request.form.get('otpcode',None)

            if code is not None in flask.session and 'email' in flask.session\
                and 'user_id' in flask.session:
                secret = current_app.config['OTP_SECRET_KEY']
                user_id = flask.session['user_id']
                totp = self.twoFaModel.generate_otp(accountname=flask.session['email'], secret=secret, interval=otp_time_interval)
                otpstatus =  totp.verify(code)
                
                if otpstatus:
                   
                    #return jsonify({'status': 'success', 'message': 'Email verified successfully!'})
                    if 'origin_request' in flask.session:
                        if flask.session['origin_request'] == 'register':
                            flash('Code verified successful', 'success')
                            return redirect(url_for('email.activate_send')) 
                         
                        # If the origin request is a sign-in request
                        elif flask.session['origin_request'] == 'signin':
                            user = self.UserModel.get_user_by_id(user_id)
                            login_user(user)
                            flask.g.user = user      
                        
                    return redirect(url_for('index'))
                else:
                    flash('Code verification failed', 'error')
        
        return render_template(self.template, title='Code verification')
            
    