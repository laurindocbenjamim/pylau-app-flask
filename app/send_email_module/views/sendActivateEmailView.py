
from typing import Any
from flask.views import View

from markupsafe import escape
from flask import request, session, redirect, url_for, flash, jsonify
from ..factory.activate_account_message_html import get_activate_account_message_html
from ..factory.emailcontroller import send_simple_email_mime_multipart

from ...token_module.userTokenModel import UserToken


class SendActivateEmailView(View):
    """
    This class is responsible for handling the sending of code verification emails to users.

    Methods:
    - dispatch_request(): Handles the GET request for sending the code verification email.
    """

    methods = ['GET']
    
    def __init__(self, userToken, userModel):
        self.userToken = userToken
        self.userModel = userModel
    
    def dispatch_request(self, user_token: str):

        """
            Handles the GET request for sending the code verification email.

            Returns:
            - If the email is sent successfully, redirects to the 2facodeverify endpoint.
            - If the email sending fails, flashes an error message and redirects to the auth.register endpoint.
        """
         
        otp_time_interval = 1440
                 
        if request.method == 'GET' and user_token is not None:
           
            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status:
                if self.userToken.is_token_expired(token):
                    flash('Token is expired!', 'danger')
                    return redirect(url_for('auth.register'))
            else:
                flash('Token required!', 'danger')
                return redirect(url_for('auth.register'))
            
            
            # Get the user details using the email address
            status, user = self.userModel.get_user_by_email(token.username)
           
            # Check if the user is identified
            if status and user is not None:
                
                if user.email == token.username:
                    email = user.email
                    lastname = user.lastname
                    firstname = user.firstname
                    
                    time_remaining = f"You have { int(otp_time_interval / 60) } hours to activate your account."
                    html = get_activate_account_message_html(str(firstname)+" "+str(lastname), token.token, time_remaining)
                    res = send_simple_email_mime_multipart('Activate account', str(email), html, False)
                    flash('An email has been sent to your email address. Please check your email to activate your account.', 'success')
                    return redirect(url_for('auth.user.login'))
                else:
                    flash('Invalid user', 'danger')
            else:
                flash('User not identified!', 'danger')  
                       
        
        return redirect(url_for('auth.register'))
            
    




