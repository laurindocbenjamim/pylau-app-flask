
from typing import Any
from flask.views import View

from flask import request,session, redirect, url_for, flash, jsonify
from ..factory.activate_account_message_html import get_activate_account_message_html
from ..factory.emailcontroller import send_simple_email_mime_multipart



class SendActivateEmailView(View):
    """
    This class is responsible for handling the sending of code verification emails to users.

    Methods:
    - dispatch_request(): Handles the GET request for sending the code verification email.
    """

    methods = ['GET']
    
    def __init__(self):
        pass
    
    def dispatch_request(self):

        """
            Handles the GET request for sending the code verification email.

            Returns:
            - If the email is sent successfully, redirects to the 2facodeverify endpoint.
            - If the email sending fails, flashes an error message and redirects to the auth.register endpoint.
        """
         
        otp_time_interval = 1440
                 
        if request.method == 'GET':
            
            if 'origin_request' and 'user_id' and 'user_token' \
                and 'firstname' and 'lastname' and 'email' in session:
               
                email = session.get('email')
                lastname = session.get('lastname')
                firstname = session.get('firstname')
                user_token = session.get('user_token')
                
                time_remaining = f"You have { int(otp_time_interval / 60) } hours to activate your account."
                html = get_activate_account_message_html(str(firstname)+" "+str(lastname), user_token, time_remaining)
                res = send_simple_email_mime_multipart('Activate account', str(email), html, False)
                flash('An email has been sent to your email address. Please check your email to activate your account.', 'success')
                return redirect(url_for('auth.user.login'))
            else:
                flash('User not identified!', 'danger')  
                       
        
        return redirect(url_for('auth.register'))
            
    




