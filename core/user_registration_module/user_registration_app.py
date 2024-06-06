


from datetime import date

from core.user_registration_module._user_create_route import _create_new_user
from core.user_registration_module.app_auth.generate_two_factor_app_auth_route import _generate_two_factor_app_auth_route
from core.user_registration_module.email_auth.send_code_to_user_email_route import _send_code_to_user_email
from core import db, clear_all_sessions

from flask import session, g, flash
from flask_cors import CORS, cross_origin

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bp = Blueprint("Register", __name__, url_prefix='/register')
CORS(bp)

"""
"""
# Fisrt step in the user registration process
# Create a new user
_create_new_user(bp, db)

# Second step in the user registration process
# Depending on the 2FA method chosen by the user,
# generate the QR code for the 2FA
# or send the OTP to the user's phone or email
_generate_two_factor_app_auth_route(bp, db)

# Send the OTP to the user's email
_send_code_to_user_email(bp, db)

# Third step in the user registration process
