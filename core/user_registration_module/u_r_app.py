

import pyotp
import datetime

from datetime import date

from core.config import generate_provisioning_uri, verify_provisioning_uri, update_imagename
from core.authmodule.repositories.create_user_final import create_final_user
from core.authmodule.controllers.two_factor_auth_controller import save_two_fa_data
from core.smtpmodule.send_html_email import send_an_html_email
from core.smtpmodule.emailcontroller import send_simple_email, send_simple_email_mime_multipart
from core.smtpmodule.html_content.activate_account_message_html import get_activate_account_message_html
from core.user_registration_module._user_create_route import create_new_user
from core import db, clear_all_sessions

from flask import session, g, flash
from flask_cors import CORS, cross_origin

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bp = Blueprint("Register", __name__, url_prefix='/register')
CORS(bp)

totp = None
user_secret_code = '37TKWDR724Z3RY7Q7B4OZDOQQWWR4A42'

"""
"""
create_new_user(bp, db)
