
import pyotp
import datetime

from ...config import get_otp_code, check_otp_code, generate_secret, generate_provisioning_uri, verify_provisioning_uri

from flask import session
from flask_cors import CORS, cross_origin

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bpapp = Blueprint("Google 2TFA", __name__, url_prefix='/2fa')
CORS(bpapp)

totp = None
secret = '37TKWDR724Z3RY7Q7B4OZDOQQWWR4A42'

@bpapp.route('/google-get', methods=['GET', 'POST'])
@cross_origin(methods=['GET'])
def get_code():
        
    if request.method == 'GET':
        otpqrcode = generate_provisioning_uri(secret)
        return render_template('auth/2fa.html', otpstatus=False, qrcodeotp=None, otpqrcode=otpqrcode)
    

@bpapp.route('/google-verify', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def chek_code():

    if request.method == 'GET':
        return render_template('auth/2fa.html', otpstatus=False, otpcode=000)

    elif request.method == 'POST':
        #OTP = request.form.get('otpcode')
        otpstatus = False

        #totp = get_otp(session['secret'])
        #otpstatus =  totp.verify(OTP)
        #return jsonify([{'otpstatus': otpstatus, 'otpcode': OTP}])
        return render_template('auth/2fa.html', otpstatus=otpstatus, otpcode=00)
   

def get_otp(secret, accountname='username', interval=40):
    totp = pyotp.TOTP(secret,name=accountname, interval=interval)

    return totp

def check_otp(OTP):
    resp = totp.verify(OTP)
    return resp

