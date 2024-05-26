
from ...config import generate_secret, generate_otp, verify_otp, get_time_remaining, hex_encoded

from flask import session

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bpapp = Blueprint("2TFA", __name__, url_prefix='/2TFA')

@bpapp.route('/gcode', methods=['GET', 'POST'])
def chek_code():

    secret = session.get('secret')
    otp = None
    otpstatus = False

    if secret:
        secret = generate_secret()
        session['secret'] = secret

        otp = generate_otp(secret)
    
        if request.method == 'POST':
            secret = session.get('secret')
            otpstatus = verify_otp(secret, otp)
            return render_template('auth/two_factor_auth.html', title='Verify 2-FA', otp=otp,otpstatus=otpstatus)
    return render_template('auth/two_factor_auth.html', title='Verify 2-FA', otp=otp, otpstatus=otpstatus)


