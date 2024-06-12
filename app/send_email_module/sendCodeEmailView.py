
import flask
from typing import Any
from flask.views import View


from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, jsonify
from .factory.otp_code_account_message_html import get_otp_code_message_html
from .factory.activate_account_message_html import get_activate_account_message_html
from .factory.generate_otp import get_otp, check_otp, generate_secret
from .emailcontroller import send_simple_email, send_simple_email_mime_multipart
from ..two_factor_auth_module.two_fa_auth_controller import load_two_fa_obj



class SendCodeEmailView(MethodView):
    methods = ['GET', 'POST']
    
    def __init__(self, twoFaModel, template):
        self.twoFaModel = twoFaModel
        self.template = template
    
    def dispatch_request(self):
        otp_time_interval = 30
                 
        if request.method == 'GET':
            
            if 'user_id' and 'two_fa_auth_method' and 'firstname' and 'lastname' and 'email' in flask.session:
               
                email = flask.session.get('email')
                lastname = flask.session.get('lastname')
                firstname = flask.session.get('firstname')
                # generate a secret code for the user
                user_secret_code = generate_secret()                
                
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

                if respTwoFa:
                    totp = get_otp(obj.two_factor_auth_secret, email , otp_time_interval)
                    OTP = totp.now()

                    time_remaining = f"This code expires in {otp_time_interval} seconds ({otp_time_interval / 60 } minutes)"
                    html = get_otp_code_message_html(str(firstname)+" "+str(lastname), OTP, time_remaining)
                    res = send_simple_email_mime_multipart('Code verification', str(email), html, False)

                    if res:
                        flash(f'If the email provided is real, a code verification was sent to <<{email}>>', 'success')
                    else:
                        flash('Email code verification failed', 'error')
                else:
                    flash('Process failed', 'error')
                    return redirect(url_for('auth.register'))

                return render_template(self.template, title='Email code verification')
            else:
                flash('User not identified!', 'danger')
                return redirect(url_for('auth.register'))
            
        elif request.method == 'POST':
            code = request.form.get('otpcode')

            if code is not None and 'two_factor_auth_secret' in flask.session and 'email' in flask.session:
                totp = get_otp(flask.session['two_factor_auth_secret'], flask.session['email'], otp_time_interval)
                otpstatus =  totp.verify(code)
                
                if otpstatus:
                    flash('Email code verification successful', 'success')
                    return redirect(url_for('auth.user.login'))
                else:
                    flash('Email code verification failed', 'error')

        return render_template(self.template, title='Email code verification')
            
    