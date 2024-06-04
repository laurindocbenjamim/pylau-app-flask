
import pyotp
import datetime

from datetime import date

from core.config import generate_provisioning_uri, verify_provisioning_uri, update_imagename
from core.authmodule.repositories.create_user_final import create_final_user
from core.authmodule.controllers.two_factor_auth_controller import save_data
from core import db

from flask import session, g
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
        if session['user_secret_code'] is None:
            return jsonify({'message': 'You are not logged in', 'status': 0, "object": session['user_secret_code'], "redirectUrl": "users/login"}, 401)
        else:
            otpqrcode = generate_provisioning_uri(session['user_secret_code'], '2FA-Authentication')
            session['otpqrcode'] = otpqrcode
            otpqrcode_uri= 'otp_qrcode_images/' + str(session['otpqrcode'])
            return render_template('auth/2fa_qrcode.html', title="2FA QRCode", otpstatus=False, 
                                   otpqrcode_uri= otpqrcode_uri, 
                                   otpqrcode=otpqrcode)    
        
    elif request.method == 'POST':
        otpcode = request.form.get('otpcode')

        if otpcode is None:
            return jsonify({'message': 'OTP code is required', 'status': 0, "object": [], "redirectUrl": "2fapp/qrcode/generate"}, 400)
        elif session['user_df']:
            secret = session['user_secret_code']
            user_df = session['user_df']
            user_id = user_df['userID']
            firstname = user_df['firstname']
            lastname = user_df['lastname']
            
            if verify_provisioning_uri(secret, otpcode):

                save_data(db, user_df['userID'], secret, session['two_fa_auth_method'])

                current_date = date.today()

                new_image_name = secret +'-otpqrcode-done-'+current_date.strftime("%Y-%m-%d")

                update_imagename('core/static/otp_qrcode_images/' + session['otpqrcode'], new_image_name)
                session.clear()
                session['firstname'] = firstname
                session['lastname'] = lastname
                #if OTP is not None and secret is not None:
                #return jsonify({'message': 'User created successfull!', 'status': 1, "object": [], "redirectUrl": "users/login"}, 200)
                return redirect(url_for('Users.success_registration'))
            return jsonify({'message': 'Invalid OTP code ', 'status': 0, "object": [], "redirectUrl": "users/login"}, 400)     
        
    

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
    


