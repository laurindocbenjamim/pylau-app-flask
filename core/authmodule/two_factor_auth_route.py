
import pyotp

from core.config import get_otp_code, check_otp_code, generate_secret

from flask import session, flash
from flask_cors import CORS, cross_origin
from core import db, clear_all_sessions
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
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bp = Blueprint("2TFA", __name__, url_prefix='/2fa')
CORS(bp)

totp = None
secret = '37TKWDR724Z3RY7Q7B4OZDOQQWWR4A42'

@bp.route('/get', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def get_code():
    
    otpstatus = False
    otp_time_interval=300
    
    if request.method == 'GET':
        session['secret'] = session['user_secret_code']

        totp = get_otp(session['secret'], 'test', 280)
        OTP = totp.now()

        return jsonify([{"OTP": OTP}])
        #return render_template('auth/2fa.html', otpstatus=False, otpcode=OTP)

@bp.route('/opt/send', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def send_code_to_user_email():
    message = ' '
    otp_time_interval=300
    type_error = ''
    otpstatus = False
    OTP = ''
    redirectUrl = url_for('2TFA.send_code_to_user_email')
    url = 'auth/2fa.html'
    user_df = []
    
    if request.method == 'GET':
        #session['user_secret_code'] = secret 
        #session.pop('user_secret_code', default=None)

        if 'user_secret_code' in session:
            user_df = session['user_df']
            activate_token = session['activate_token']
            user_id = user_df['userID']
            secret = session['user_secret_code']
            auth_method = session['two_fa_auth_method']

            totp = get_otp(session['user_secret_code'], user_df['email'], otp_time_interval)
            OTP = totp.now()

            time_remaining = f"This code expires in {otp_time_interval} seconds ({otp_time_interval / 60 } minutes)"

            html = get_otp_code_message_html(str(user_df['firstname'])+" "+str(user_df['lastname']), OTP, time_remaining)
            res = send_simple_email_mime_multipart('Code verification', str(user_df['email']), html, False)
            
            if res:
                res = save_two_fa_data(db, user_id, secret, auth_method)

                message = "Enter the code sent to your email to verify your account"
                type_error = 'success'
                
            else:
                message = f"Failed to send code to {str(user_df['email'])}"
                type_error = 'error'
                redirectUrl = '2TFA.send_code_to_user_email'
        else:
            message = f"User not found "
            type_error = 'error'
    elif request.method == 'POST':
        code = request.form.get('otpcode')
        if code is None:
            message = f"OTP code is required"
            type_error = 'error'
        elif 'user_secret_code' not in session:
            message = f"User not found"
            type_error = 'error'
        elif 'activate_token' not in session:
            message = f"User not found"
            type_error = 'error'
        elif 'user_df' not in session:
            message = f"User not found"
            type_error = 'error'
        else:
            user_df = session['user_df']
            
            # this is the user's secret code
            totp = get_otp(session['user_secret_code'], user_df['email'], otp_time_interval)
            otpstatus =  totp.verify(code)
            if otpstatus:
                message = f"Code verified successfully"
                type_error = 'success'
                time_remaining = "You have 14 days to activate your account. After that, you will need to request a new code."
                html2 = get_activate_account_message_html(str(user_df['firstname'])+" "+str(user_df['lastname']), session['activate_token'], time_remaining)
                res = send_simple_email_mime_multipart('Activate your account', str(user_df['email']), html2, False)
                
                clear_all_sessions()

                flash(message, type_error)
                return redirect(url_for('Users.success_registration'))
            else:
                message = f"Invalid code. Please try again requesting a new code."
                type_error = 'error'
                redirectUrl = '2TFA.send_code_to_user_email'
    
        
    flash(message, type_error)
    return render_template(url, otpstatus=False, otpcode=00, redirectUrl=redirectUrl)
    

@bp.route('/verify', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def chek_code():

    if request.method == 'GET':
        return render_template('auth/2fa.html', otpstatus=False, otpcode=000)

    elif request.method == 'POST':
        OTP = request.form.get('otpcode')
        otpstatus = False

        totp = get_otp(secret, 'test', 280)
        otpstatus =  totp.verify(OTP)

        if otpstatus:
            if 'activate_token' not in session:
                return jsonify([{'otpstatus': otpstatus, 'otpcode': OTP}])
            else:
                return jsonify([{'otpstatus': otpstatus, 'otpcode': OTP}])
        return jsonify([{'otpstatus': otpstatus, 'otpcode': OTP}])
        #return render_template('auth/2fa.html', otpstatus=otpstatus, otpcode=OTP)
       

@bp.route('/verify-otp-code', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def get_code_by_email():
    
    otpstatus = False
    otp_time_interval=300
    redirectUrl = url_for('2TFA.get_code_by_email')
    
    if request.method == 'GET':
        if 'two_factor_auth_secret' not in session:
            error = 'User not found'
        elif 'email' not in session:
            error = 'User not found'
        else:
            secret = session['two_factor_auth_secret']
            email = session['email']
            firstname = session['firstname']
            lastname = session['lastname']
            otp_time_interval = 300

            totp = get_otp(secret, email, otp_time_interval)
            OTP = totp.now()

            time_remaining = f"This code expires in {otp_time_interval} seconds ({otp_time_interval / 60 } minutes)"

            html = get_otp_code_message_html(str(firstname)+" "+str(lastname), OTP, time_remaining)
            res = send_simple_email_mime_multipart('Code verification', str(email), html, False)
            error = f'A code was sent to the email {str(email)}'
            if res:
                #return jsonify([{"OTP": OTP}])
                flash(error, 'success')
                return render_template('auth/2fa.html', otpstatus=False, otpcode=OTP, redirectUrl=redirectUrl, user_df=[
                    {'firstname': firstname, 'lastname': lastname, 'email': email}
                ])
            
            flash('Failed to send code to email', 'error')
        return redirect(url_for('2TFA.get_code_by_email'))
    elif request.method == 'POST':
        code = request.form.get('otpcode')
        totp = get_otp(session['two_factor_auth_secret'], session['email'], 300)
        otpstatus =  totp.verify(code)
        
        if otpstatus:
            firstname = session['firstname']
            lastname = session['lastname']
            flash('Code verified successfully', 'success')
            return redirect(url_for('public_projects'))
        return redirect(url_for('2TFA.get_code_by_email'))       

def get_otp(secret, accountname, interval):
    totp = pyotp.TOTP(secret,name=accountname, interval=interval)
    return totp

def check_otp(OTP, secret, user, otp_time_interval):
    totp = get_otp(secret, user, otp_time_interval)     
    return totp.verify(OTP)

