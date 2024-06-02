
import pyotp
import datetime

from ...config import get_otp_code, check_otp_code, generate_secret, generate_provisioning_uri, verify_provisioning_uri

from flask import session
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
@bp.route('/get', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def get_code():
        
    if request.method == 'GET':
        #return jsonify({'secret': user_secret_code})
        otpqrcode = generate_provisioning_uri(session['user_secret_code'], '2FA-Authentication')
        return render_template('auth/two_factor_app_auth.html', otpstatus=False, qrcodeotp=None, otpqrcode=otpqrcode)
    

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
   

