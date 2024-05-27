
from ...config import get_otp_code, check_otp_code, generate_secret

from flask import session

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bpapp = Blueprint("2TFA", __name__, url_prefix='/2fa')

totp = None

@bpapp.route('/get', methods=['GET', 'POST'])
def get_code():
    secret = generate_secret()
    session['secret'] = secret

    otpstatus = False

    code = get_otp_code(session['secret'])

    return jsonify([{'otpstatus': otpstatus, "code": code, "secret": session['secret']}])

@bpapp.route('/<code>/check', methods=['GET', 'POST'])
def chek_code(code):
    otpstatus = False

    otpstatus = check_otp_code(session['secret'], code)

    return jsonify([{'otpstatus': otpstatus, 'otpcode': code, 'secret': session['secret']}])
   


