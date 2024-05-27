
import pyotp
import datetime

from ...config import get_otp_code, check_otp_code, generate_secret

from flask import session

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bpapp = Blueprint("2TFA", __name__, url_prefix='/2fa')

totp = None

@bpapp.route('/get', methods=['GET', 'POST'])
def get_code():
    secret = '37TKWDR724Z3RY7Q7B4OZDOQQWWR4A42'
    session['secret'] = secret

    totp = get_otp(session['secret'])
    OTP = totp.now()

    #return jsonify([{"OTP": OTP}])
    return render_template('auth/2fa.html', otpstatus=False, otpcode=OTP)

@bpapp.route('/<OTP>/check', methods=['GET', 'POST'])
def chek_code(OTP):
    otpstatus = False

    totp = get_otp(session['secret'])
    otpstatus =  totp.verify(OTP)
    #return jsonify([{'otpstatus': otpstatus, 'otpcode': OTP}])
    return render_template('auth/2fa.html', otpstatus=otpstatus, otpcode=OTP)
   

def get_otp(secret, accountname='username', interval=40):
    totp = pyotp.TOTP(secret,name=accountname, interval=interval)

    return totp

def check_otp(OTP):
    resp = totp.verify(OTP)
    return resp

