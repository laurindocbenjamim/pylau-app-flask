
import pyotp
import datetime

from datetime import date

from core.config import generate_provisioning_uri, verify_provisioning_uri, update_imagename
from core.authmodule.repositories.create_user_final import create_final_user
from core.authmodule.controllers.two_factor_auth_controller import save_data
from core.smtpmodule.send_html_email import send_an_html_email
from core.smtpmodule.emailcontroller import send_simple_email, send_simple_email_mime_multipart
from core.smtpmodule.html_content.activate_account_message_html import get_activate_account_message_html
from core import db

from flask import session, g, flash
from flask_cors import CORS, cross_origin

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bp = Blueprint("2FApp", __name__, url_prefix='/2fapp')
CORS(bp)

totp = None
user_secret_code = '37TKWDR724Z3RY7Q7B4OZDOQQWWR4A42'

"""
"""

# Google 2FA
@bp.route('/qrcode/generate', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def generate_qr_code():
        
    if request.method == 'GET':
        #if g.user is None:
        error = None
        if session['user_secret_code'] is None:
            error = 'This user was not found!'
            #return jsonify({'message': error, 'status': 0, "object": session['user_secret_code'], "redirectUrl": "users/login"}, 401)
            flash(error)
            return redirect(url_for('Users.sign_up'))
        else:
            user_df = session['user_df']
            email = user_df['email']
            otpqrcode = generate_provisioning_uri(session['user_secret_code'], email)
            session['otpqrcode'] = otpqrcode
            session['otpqrcode_uri'] = 'otp_qrcode_images/' + str(session['otpqrcode'])
            return render_template('auth/2fa_qrcode.html', title="2FA QRCode", otpstatus=False, 
                                   otpqrcode_uri= session['otpqrcode_uri'], 
                                   otpqrcode=otpqrcode)    
        
    elif request.method == 'POST':
        otpcode = request.form.get('otpcode')

        if otpcode is None and session['user_secret_code'] is not None:
            error = 'OTP code is required'
            #flash(error)
            #return jsonify({'message': 'OTP code is required', 'status': 0, "object": [], "redirectUrl": "2fapp/qrcode/generate"}, 400)
            return render_template('auth/2fa_qrcode.html', title="2FA QRCode", otpstatus=False, message=error,
                                   otpqrcode_uri= session['otpqrcode_uri'], 
                                   otpqrcode=session['otpqrcode'])
        elif session['user_df'] and session['user_secret_code'] is not None:
            secret = session['user_secret_code']
            user_df = session['user_df']
            user_id = user_df['userID']
            firstname = user_df['firstname']
            lastname = user_df['lastname']
            email = user_df['email']
            
            if verify_provisioning_uri(secret, otpcode):

                save_data(db, user_df['userID'], secret, session['two_fa_auth_method'])

                current_date = date.today()

                new_image_name = secret +'-otpqrcode-done-'+current_date.strftime("%Y-%m-%d")

                update_imagename('core/static/otp_qrcode_images/' + session['otpqrcode'], new_image_name)
                session.clear()
                session['firstname'] = firstname
                session['lastname'] = lastname

                html = get_activate_account_message_html(str(firstname)+" "+str(lastname), user_id)
                res = send_simple_email_mime_multipart('Activate your account', email, html, False)

                #send_an_html_email("Test Active email", email, user_id, str(firstname) + ' ' + str(lastname), "Ola")
                #if OTP is not None and secret is not None:
                #return jsonify({'message': 'User created successfull!', 'status': 1, "object": [], "redirectUrl": "users/login"}, 200)
                return redirect(url_for('Users.success_registration'))
            elif session['user_secret_code'] is not None:
                return redirect(url_for('2FApp.generate_qr_code'))
            #return jsonify({'message': 'Invalid OTP code ', 'status': 0, "object": [], "redirectUrl": "users/login"}, 400)
        return redirect(url_for('Auth.signin'))        
    

# Google 2FA
@bp.route('/verify/<code>', methods=['GET', 'POST'])
@bp.route('/verify', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def chek_code(code=None):

    if request.method == 'GET':
        if code is not None:
            return render_template('auth/two_factor_app_auth.html', title="2FA-Authentication", otpstatus=False, qrcodeotp=None, verify_code=1)
        else:            
            session['user_secret_code'] = user_secret_code
            otpqrcode = generate_provisioning_uri(session['user_secret_code'])
            return render_template('auth/two_factor_app_auth.html', title="2FA-Authentication", otpstatus=False, qrcodeotp=None, otpqrcode=otpqrcode)
    
    elif request.method == 'POST':
        OTP = request.form.get('otpcode')
        otpstatus = False

        otpstatus = verify_provisioning_uri(session['user_secret_code'], OTP)
        #return jsonify([{'otpstatus': otpstatus, 'otpcode': OTP}])
        return render_template('auth/two_factor_app_auth.html', otpstatus=otpstatus)
    


