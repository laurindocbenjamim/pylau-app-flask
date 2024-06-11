
import flask
from typing import Any
from flask.views import View

from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, jsonify
from .factory.otp_code_account_message_html import get_otp_code_message_html
from .factory.activate_account_message_html import get_activate_account_message_html
from .factory.generate_otp import get_otp, check_otp, generate_secret
from .emailcontroller import send_simple_email, send_simple_email_mime_multipart

class SendCodeEmailView(MethodView):
    methods = ['GET', 'POST']
    
    def __init__(self, template):
        #self.model = model
        self.template = template
    
    def dispatch_request(self):
        otp_time_interval = 30
        #email = flask.session.get('email')
        #lastname = flask.session.get('lastname')
        #firstname = flask.session.get('firstname')
        
        email = 'rocketmc2009@gmail.com'  
        firstname = 'Laurindo'
        lastname = "laurindo"

         
        if request.method == 'GET':
                           
            user_secret_code = generate_secret()
            flask.session['two_factor_auth_secret'] = user_secret_code
            flask.session['email'] = email
            flask.session['firstname'] = firstname
            flask.session['lastname'] = lastname
            totp = get_otp(user_secret_code, email , otp_time_interval)
            OTP = totp.now()

            time_remaining = f"This code expires in {otp_time_interval} seconds ({otp_time_interval / 60 } minutes)"
            html = get_otp_code_message_html(str(firstname)+" "+str(lastname), OTP, time_remaining)
            res = send_simple_email_mime_multipart('Code verification', str(email), html, False)

            if res:
                flash(f'A code verification was sent to <<{email}>>', 'success')
            else:
                flash('Email code verification failed', 'error')
            return render_template(self.template, title='Email code verification')
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
            
    