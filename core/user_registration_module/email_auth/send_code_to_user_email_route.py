
import pyotp

from core.config import get_otp_code, check_otp_code, generate_secret

from flask import session, flash
from flask_cors import CORS, cross_origin
from core import db, clear_all_sessions, generate_simple_otp, check_simple_otp
from core import (
    validate_form_fields, is_valid_email,
    check_email_exists, check_phone_exists, create_user,
    generate_token
)

from core.authmodule.controllers.two_factor_auth_controller import save_two_fa_data
from core.smtpmodule.emailcontroller import send_simple_email, send_simple_email_mime_multipart
from core.smtpmodule.html_content.activate_account_message_html import get_activate_account_message_html
from core.smtpmodule.html_content.otp_code_account_message_html import get_otp_code_message_html

from flask import (
    render_template, url_for, request, redirect, jsonify
)




# Send the OTP to the user's email Route
def _send_code_to_user_email(bp, db):
    @bp.route('/send/opt/email', methods=['GET', 'POST'])
    @cross_origin(methods=['GET', 'POST'])
    def _send_code_to_user_email():
        
        otp_time_interval=300
        type_message = message=OTP = redirectUrl = ''
        otpstatus = False

        url = 'auth/2fa.html'
        user_df = []
        
        # Check if the request method is GET
        if request.method == 'GET':
            #session['user_secret_code'] = secret 
            #session.pop('user_secret_code', default=None)
            
            check_the_user_email_with_otp(otp_time_interval)
            
        elif request.method == 'POST':
            code = request.form.get('otpcode')
            if code is None:
                message = f"OTP code is required"
                type_message = 'error'
                
            elif is_session_exists():
                user_df = session['user_df']
                
                # this is the user's secret code
                totp = generate_simple_otp(session['user_secret_code'], user_df['email'], otp_time_interval)
                otpstatus =  totp.verify(code)
                if otpstatus:
                    message = f"Code verified successfully. Check your email to activate your account."
                    type_message = 'success'
                    time_remaining = "You have 14 days to activate your account. After that, you will need to request a new code."
                    fullname = str(user_df['firstname'])+" "+str(user_df['lastname'])
                    
                    # Get the HTML content for the OTP code message
                    html2 = get_activate_account_message_html(fullname, session['activate_token'], time_remaining)
                    # Send the OTP code to the user's email
                    res = send_simple_email_mime_multipart('Activate your account', str(user_df['email']), html2, False)
                    
                    clear_all_sessions()
                    session['name'] = fullname
                    session['email'] = user_df['email']
                    flash(message, type_message)
                    return redirect(url_for('Users.success_registration'))
                else:
                    message = f"Invalid code. Please try again requesting a new code."
                    type_message = 'error'
                    redirectUrl = 'Register._send_code_to_user_email'
        
            
        flash(message, type_message)
        return render_template(url, otpstatus=False, otpcode=00, redirectUrl=redirectUrl)
        


def check_the_user_email_with_otp(otp_time_interval):
    otp_time_interval=300
    type_message = message=OTP = redirectUrl = ''   
    url = 'auth/2fa.html'
 
    # Check if the user_secret_code is not in the session
  
    if is_session_exists():
        redirectUrl=message=type_message = ''
        user_df = session['user_df']
        activate_token = session['activate_token']
        user_id = user_df['userID']
        secret = session['user_secret_code']
        auth_method = session['two_fa_auth_method']

        # Generate the OTP code through the user email and secret code
        totp = generate_simple_otp(session['user_secret_code'], user_df['email'], otp_time_interval)
        OTP = totp.now()

        time_remaining = f"This code expires in {otp_time_interval} seconds ({otp_time_interval / 60 } minutes)"

        # Get the HTML content for the OTP code message
        html = get_otp_code_message_html(str(user_df['firstname'])+" "+str(user_df['lastname']), OTP, time_remaining)
        # Send the OTP code to the user's email
        res = send_simple_email_mime_multipart('Code verification', str(user_df['email']), html, False)
                
        if res:
            # if true, save the 2FA data to the database
            res = save_two_fa_data(db, user_id, secret, auth_method)

            message = f"Enter the code sent to your email <<{str(user_df['email'])}>> to verify your account"
            type_message = 'success'
                    
        else:
            message = f"Failed to send code to {str(user_df['email'])}. Please try again later."
            type_message = 'error'
            redirectUrl = 'register/send/opt/email'
    flash(message, type_message)
    return render_template(url, otpstatus=False, otpcode=00, redirectUrl=redirectUrl)



# validate sessions
def is_session_exists():
    if 'user_secret_code' and 'user_df' and 'activate_token' and 'two_fa_auth_method' in session:
        message = 'Failed to check the user indentity!'        
        return True
    flash('Failed to check the user indentity!', 'error')
    return redirect(url_for('Auth.signin'))
           