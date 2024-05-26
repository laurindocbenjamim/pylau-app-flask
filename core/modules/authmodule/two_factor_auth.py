
from ...config import get_otp, check_otp, generate_secret

from flask import session

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bpapp = Blueprint("2TFA", __name__, url_prefix='/2fa')

@bpapp.route('/gcode', methods=['GET', 'POST'])
def chek_code():
    secret = generate_secret()
    secret = session.get('secret')
    otp = None
    otpstatus = False

    otp = get_otp(secret)

    return jsonify({'otpstatus': otpstatus, 'otp': otp.now()})
   


