
import functools

import re
from datetime import date

from flask import (
    Blueprint, flash, g, redirect, render_template, make_response, request, session, url_for,jsonify,
    abort
)
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
from core import db
from core import create_user, get_users, get_user_by_id, update_user, delete_user, check_email_exists, check_phone_exists
from core.config import generate_secret, generate_provisioning_uri, verify_provisioning_uri, update_imagename

bp = Blueprint('users', __name__, url_prefix='/users')    # Create a Blueprint object
CORS(bp)

from core.authmodule.getalluser import get_allusers
import requests
# Loading block of routes
get_allusers(bp, db)



@bp.route('/create', methods=['GET', 'POST'])   # Define a route for the login page
@cross_origin(methods=['GET', 'POST'])
def sign_up():

    message = None
    session['user_secret_code'] = None 
    session['otpqrcode'] = None

    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        country = request.form.get('country')
        country_code = request.form.get('country_code')
        phone = request.form.get('phone')
        two_factor_auth_code = request.form.get('two_factor_auth_code')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        
        # validate the fields
        validate_for(firstname, lastname, email, country,
            country_code, phone, password, confirm, '123456')
        
        # check if email is valid
        if is_valid_email(email) == False:
            return jsonify({'message': 'Invalid email address', 'status': 'error', "redirectUrl": "users/create"}, 400)
        
        # check if email exists
        if check_email_exists(email):
            return jsonify({'message': 'Email already exists', 'status': 'error', "redirectUrl": "users/create"}, 400)
        
        # check if phone exists
        if check_phone_exists(phone):
            return jsonify({'message': 'Phone already exists', 'status': 'error', "redirectUrl": "users/create"}, 400)
        
        # hash the password
        password_hash = generate_password_hash(password)

        if not check_password_hash(password_hash, confirm):
            return jsonify({'message': 'The passwords do not match', 'status': 'error', "object": [], "redirectUrl": "users/create"}, 400)

        # check if the passwords match
        if two_factor_auth_code == '':
                        
            if session.get('user_secret_code') is None and session.get('otpqrcode') is None:
                session['user_secret_code'] = generate_secret()
                        
                session['otpqrcode'] = generate_provisioning_uri(session['user_secret_code'], email)
            
                return jsonify({'message': 'The OTP QrCode has been generated successfully! Scan the QR code to get the OTP code', 
                                'status': 2, "object": [], "redirectUrl": "users/create",
                                'secret': session.get('user_secret_code'),
                                "otpqrcode": session['otpqrcode'],
                                "otpqrcode_uri": 'static/otp_qrcode_images/' + str(session['otpqrcode'])
                                }, 200)            

        else:
            if len(two_factor_auth_code) != 6:
                return jsonify({'message': 'Maximum digits required for the 2FA code is 6.', 'status': 'error', "redirectUrl": "users/create"}, 400)
            else:

                OTP = request.form.get('two_factor_auth_code')
                secret = request.form.get('secret')
                
                otpstatus = False
                if OTP is not None and secret is not None:
                    otpstatus = verify_provisioning_uri(secret, OTP)

                    if otpstatus:
                        user = create_user(db,firstname, lastname, email, country,country_code, phone, password_hash, secret)
                        if user.userID is not None:
                            img = request.form.get('otpqrcode')
                            current_date = date.today()
                            new_image_name = secret +'-otpqrcode-done-'+current_date.strftime("%Y-%m-%d")
                            update_imagename('core/static/otp_qrcode_images/' + img, new_image_name)

                            return jsonify({'message': 'User is ready to be created successfully!', 'status': 3, 'otpstatus':otpstatus, 
                                            "object": request.form, "redirectUrl": "auth/2fapp/login"}, 200)
                        else:              
                            return jsonify({'message': 'Failed to regist user', 'status': 'error', "redirectUrl": "users/create"}, 400)
                    else:
                        return jsonify({'message': '2FA OTP code is invalid.', 'status': 'error', "redirectUrl": "users/create"}, 400)
                else:                 
                    return jsonify({'message': '2FA OTP code not found.', 'status': 'error', 'otpstatus':otpstatus, 
                                            "object": request.form, "redirectUrl": "users/create"}, 400)

        
            # create a user
            """user = create_user(db,firstname, lastname, email, country,country_code, phone, password_hash, two_factor_auth_code)
            # get all users
            users = get_users(db)
             
        
        if email == 'rocketmc2009@gmail.com' and password == 'admin':
            return jsonify({'message': "User created successfully!",'Content-Type': 'application/json', "object": users, "redirectUrl": "2fapp/verify" }, 200)
        else:
            return jsonify({'message': message, "user_created": user, "object": users, "redirectUrl": "users/create" }, 400)
            """
    return render_template('auth/register.html', title='Sign Up')

# get all users
@bp.route('/get-all', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def get_all_users():
    users = get_users(db)
    
    return jsonify({'message': 'Users found', 'data': users})
    #return f"User logged in successfully: {user.username}"

# get user by id
@bp.route('/<userid>/get', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def getuser_by_id(userid):
    users = get_user_by_id(db, userid)
    
    return jsonify([{'message': 'User found', 'data': users}])
    #return f"User logged in successfully: {user.username}"


# Update user
@bp.route('/update', methods=['POST'])    # 
@cross_origin(methods=['POST'])
def update_user():
    username = request.form.get('username')
    password = request.form.get('password')
    id = request.form.get('id')

    obj = update_user(db, 'Gamba', 'roooooooooot', 1)

    users = get_users(db)
    return jsonify([{'message': 'User updated successfully', 'data': users}])

# Delete a usergit 
@bp.route('/<userid>/delete', methods=['GET'])    #
@cross_origin(methods=['GET'])
def deleteuser(userid):
    
    delete_user(db, userid)
    users = get_users(db)
    return jsonify([{'message': 'User deleted successfully', 'data': users}])




def capture_user_info():
    # Get User IP
    user_ip = request.remote_addr

    # Get User Mac Address
    user_mac = requests.get('https://api.macvendors.com').text

    # Get User Device Type
    user_agent = request.user_agent
    user_device = user_agent.platform

    return user_ip, user_mac, user_device

def validate_for(firstname, lastname, email, country,
            country_code, phone, password, confirm, two_factor_auth_code):
        # Validate each field
        if not firstname or not isinstance(firstname, str):
            return jsonify({'message': 'First name is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not lastname or not isinstance(lastname, str):
            return jsonify({'message': 'Last name is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not email or not isinstance(email, str):
            return jsonify({'message': 'Email is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not country or not isinstance(country, str):
            return jsonify({'message': 'Country is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not country_code or not isinstance(country_code, str):
            return jsonify({'message': 'Country code is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not phone or not isinstance(phone, str):
            return jsonify({'message': 'Phone is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not two_factor_auth_code or not isinstance(two_factor_auth_code, str):
            return jsonify({'message': 'Two-factor authentication code is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not password or not isinstance(password, str):
            return jsonify({'message': 'Password is required', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if not confirm or not isinstance(confirm, str):
            return jsonify({'message': 'Confirm password is required', 'status': 'error', "redirectUrl": "users/create"}, 400)

        # Filter unauthorized characters
        authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        if any(char not in authorized_chars for char in firstname):
            return jsonify({'message': 'Invalid characters in first name', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if any(char not in authorized_chars for char in lastname):
            return jsonify({'message': 'Invalid characters in last name', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if any(char not in authorized_chars for char in country):
            return jsonify({'message': 'Invalid characters in country', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if any(char not in authorized_chars for char in country_code):
            return jsonify({'message': 'Invalid characters in country code', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if any(char not in authorized_chars for char in phone):
            return jsonify({'message': 'Invalid characters in phone', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if any(char not in authorized_chars for char in two_factor_auth_code):
            return jsonify({'message': 'Invalid characters in two-factor authentication code', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if any(char not in authorized_chars for char in password):
            return jsonify({'message': 'Invalid characters in password', 'status': 'error', "redirectUrl": "users/create"}, 400)
        if any(char not in authorized_chars for char in confirm):
            return jsonify({'message': 'Invalid characters in confirm password', 'status': 'error', "redirectUrl": "users/create"}, 400)
        


def is_valid_email(email):
    if not email or not isinstance(email, str):
        return False

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, email) is not None:
        domain = email.split('@')[1]
        if domain.endswith('gmail.com') or domain.endswith('outlook.com') or domain.endswith('hotmail.com') or domain.endswith('live.com') or domain.endswith('icloud.com'):
            return True
    return False
