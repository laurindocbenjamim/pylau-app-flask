
import pyotp
import datetime

from core.config import generate_provisioning_uri, verify_provisioning_uri

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
@bp.route('/qrcode/get', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def get_qr_code():
        
    if request.method == 'GET':
        #if g.user is None:
        if session['user_secret_code'] is None:
            return jsonify({'message': 'You are not logged in', 'status': 0, "object": session['user_secret_code'], "redirectUrl": "users/login"}, 401)
        else:
            #return jsonify({'secret': user_secret_code})
            otpqrcode = generate_provisioning_uri(session['user_secret_code'], '2FA-Authentication')
            session['otpqrcode'] = otpqrcode
            otpqrcode_uri= 'otp_qrcode_images/' + str(session['otpqrcode'])
            return render_template('auth/2fa_qrcode.html', title="2FA QRCode", otpstatus=False, 
                                   otpqrcode_uri= otpqrcode_uri, 
                                   otpqrcode=otpqrcode)
            #return jsonify({'message': 'The OTP QrCode has been generated successfully! Scan the QR code to get the OTP code', 
                                        #'status': 2, "object": [], "redirectUrl": "users/create",
                                        #'secret': session.get('user_secret_code'),
                                        #"otpqrcode": session['otpqrcode'],
                                        #"otpqrcode_uri": 'static/otp_qrcode_images/' + str(session['otpqrcode'])
                                        #}, 200)          
        
    

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
   

