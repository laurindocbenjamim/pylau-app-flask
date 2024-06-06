
import pyotp
import datetime

from datetime import date

from core.config import generate_provisioning_uri, verify_provisioning_uri, update_imagename
from core.authmodule.repositories.create_user_final import create_final_user
from core.authmodule.controllers.two_factor_auth_controller import save_two_fa_data
from core.smtpmodule.send_html_email import send_an_html_email
from core.smtpmodule.emailcontroller import send_simple_email, send_simple_email_mime_multipart
from core.smtpmodule.html_content.activate_account_message_html import get_activate_account_message_html
from core import db, clear_all_sessions

from flask import session, g, flash
from flask_cors import cross_origin

from flask import (
    render_template, url_for, request, redirect, jsonify
)

"""
"""

def _generate_two_factor_app_auth_route(bp, db):
    # Google 2FA
    @bp.route('/qrcode/generate', methods=['GET', 'POST'])
    @cross_origin(methods=['GET'])
    def generate_qr_code():
        message = ''
        type_message = ''
        redirectURL = 'register/qrcode/generate'

        # Check if the request method is GET
        if request.method == 'GET':
            #if g.user is None:
           
            # Check if the user_secret_code is not in the session
            if 'user_secret_code' not in session:
                message = 'This user was not found!'
                type_message = 'error'
                redirectURL = 'Register.sign_up'

            # Check if the user_df is not in the session   
            elif 'user_df' not in session:                    
                    message = 'User not identified!'
                    type_message = 'error'
                    redirectURL = 'Register.sign_up'             
            else:
                # Get the user_df from the session
                user_df = session['user_df']
                email = user_df['email']

                # Generate the provisioning URI
                otpqrcode = generate_provisioning_uri(session['user_secret_code'], email)
                session['otpqrcode'] = otpqrcode
                session['otpqrcode_uri'] = 'otp_qrcode_images/' + str(session['otpqrcode'])

                # Return the 2FA QRCode template with the OTP QRCode image
                flash("Scan the QrCode with your authenticate application", 'info')
                return render_template('auth/2fa_qrcode.html', title="2FA QRCode", otpstatus=False, 
                                    otpqrcode_uri= session['otpqrcode_uri'], 
                                    otpqrcode=otpqrcode)    
            
        elif request.method == 'POST':
            otpcode = request.form.get('otpcode')

            if otpcode is None:
                message = 'OTP code is required'
                type_message = 'error'
            elif 'user_df' not in session:
                message = 'OTP code is required'
                type_message = 'error'
            elif 'user_secret_code' not in session:
                message = 'OTP code is required'
                type_message = 'error'
            elif 'otpqrcode_uri' not in session:
                message = 'OTP code is required'
                type_message = 'error'
            elif 'otpqrcode' not in session:
                message = 'OTP code is required'
                type_message = 'error'            
            elif 'activate_token' not in session:
                message = 'User not identified!'
                type_message = 'error'
            else:
                # Get the secret code from the session
                check_provisioning_app_auth_code(otpcode)

            # Redirect to the sign_up route if not passed the validation
            flash(message, type_message)
            return redirect(url_for('Auth.signin'))        



"""
This function checks the OTP code entered by the user
in order to activate the user account
"""
def check_provisioning_app_auth_code(otpcode):

    # Get the secret_code and the user_df from the session
    secret = session['user_secret_code']
    user_df = session['user_df']
    user_id = user_df['userID']
    firstname = user_df['firstname']
    lastname = user_df['lastname']
    email = user_df['email']
    
    # Verify the provisioning URI
    if verify_provisioning_uri(secret, otpcode):
        
        # Save the 2FA data in the database
        save_two_fa_data(db, user_df['userID'], secret, session['two_fa_auth_method'])
        # Get the current date
        current_date = date.today()
        # generate a new name for the qr code image
        new_image_name = secret +'-otpqrcode-done-'+current_date.strftime("%Y-%m-%d")

        # Update the image name in the directory
        update_imagename('core/static/otp_qrcode_images/' + session['otpqrcode'], new_image_name)
        
        # Set the user information in the session
        session['firstname'] = firstname
        session['lastname'] = lastname
        fullname = str(firstname) + ' ' + str(lastname)
        time_remaining = "You have 14 days to activate your account. After that, you will need to request a new code."

        # Get the html content for the email message
        html = get_activate_account_message_html(fullname, session['activate_token'], time_remaining)
        # Send the email message to the user
        res = send_simple_email_mime_multipart('Activate your account', email, html, False)

        # Clear all the sessions
        clear_all_sessions()
        session.clear()
        # Flash a success message to the user
        flash('User created successfull! Check your email <<'+ email+ '>> to activate your account.', 'success')
        
        return render_template("auth/success_registration.html", title="Success Registration", 
                               email=email, name=fullname, redirectURL='Auth.signin') 
    return redirect(url_for('Register.sign_up'))
    
