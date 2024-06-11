
import flask
from typing import Any
from flask.views import View

from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, jsonify
from factory.otp_code_account_message_html import get_otp_code_message_html
from factory.activate_account_message_html import get_activate_account_message_html
from factory.generate_otp import get_otp, check_otp, generate_secret
from .emailcontroller import send_simple_email, send_simple_email_mime_multipart

class SendCodeEmailView(MethodView):
    methods = ['GET', 'POST']
    
    def __init__(self, model, template):
        self.model = model
        self.template = template
    
    def dispatch_request(self, **kwargs):
        otp_time_interval = 30
        email = kwargs.get('email')
        lastname = kwargs.get('lastname')
        firstname = kwargs.get('firstname')
         
        if request.method == 'GET':
                           
            user_secret_code = generate_secret()
            totp = get_otp(user_secret_code, email , otp_time_interval)
            OTP = totp.now()

            time_remaining = f"This code expires in {otp_time_interval} seconds ({otp_time_interval / 60 } minutes)"
            html = get_otp_code_message_html(str(firstname)+" "+str(lastname), OTP, time_remaining)
            res = send_simple_email_mime_multipart('Code verification', str(email), html, False)
            if res:
                flash('Email code verification failed', 'info')
            else:
                flash('Email code verification sent', 'success')
        return render_template(self.template)
    