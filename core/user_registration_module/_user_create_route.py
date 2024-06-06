
import functools

import re
import requests

from datetime import date
from flask import jsonify, g, session, request, render_template, redirect, url_for
from flask_cors import cross_origin
from core import (
    validate_form_fields, is_valid_email,
    check_email_exists, check_phone_exists, create_user,
    generate_token
)

from core import get_user_by_email, get_user_by_id
from core.authmodule.repositories.create_user_final import create_final_user
from core import create_token
from werkzeug.security import check_password_hash, generate_password_hash
from core.config import generate_secret, generate_provisioning_uri, verify_provisioning_uri, update_imagename


def create_new_user(bp, db):
    @bp.route('/create', methods=['GET', 'POST'])   # Define a route for the login page
    @cross_origin(methods=['GET', 'POST'])
    def sign_up():

        error = None
        redirectURL = None
        url_status = 400
        status = 'error'
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
            two_fa_auth_method = request.form.get('two_fa_auth_method')

            if two_fa_auth_method is None:
                return jsonify({'message': 'The 2FA auth method is required.', 'status': 'error', "redirectUrl": "users/create"}, url_status)
            
            # validate the fields
            validate_form_fields(firstname, lastname, email, country,
                country_code, phone, password, confirm, '123456')
            
            # check if email is valid
            if is_valid_email(email) == False:
                return jsonify({'message': 'Invalid email address. Accepted emails: gmail.com, outlook.com, hotmail.com, live.com, icloud.com', 'status': 'error', "redirectUrl": "users/create"}, 400)
            
            # check if email exists
            if check_email_exists(email):
                return jsonify({'message': 'Email already exists', 'status': 'error', "redirectUrl": "users/create"}, url_status)
            
            # check if phone exists
            if check_phone_exists(phone):
                return jsonify({'message': 'Phone already exists', 'status': 'error', "redirectUrl": "users/create"}, url_status)
            
            # hash the password
            password_hash = generate_password_hash(password)

            if not check_password_hash(password_hash, confirm):
                return jsonify({'message': 'The passwords do not match', 'status': 'error', "object": [], "redirectUrl": "users/create"}, url_status)

            # check if the passwords match
            if two_factor_auth_code == '':
                            
                if session.get('user_secret_code') is None and session.get('otpqrcode') is None:
                    session['user_secret_code'] = generate_secret()
                    session['two_fa_auth_method'] = two_fa_auth_method
                            
                    #session['otpqrcode'] = generate_provisioning_uri(session['user_secret_code'], email)
                    obj = create_user(db,firstname, lastname, email, country,country_code, phone, password_hash)
                    
                    if obj is not None:
                        session['user_df'] = obj
                        #g.user = obj
                        token = generate_token(obj['email'])
                        url_status = 400 
                        response = create_token(db, obj['userID'], token, 14)

                        if response is None:
                            error = 'Failed to create user. Please try again later.'
                            redirectURL = "users/create"
                            url_status = 400                            
                        else:
                            url_status = 200
                            status = 2
                            error = 'User created successfully!: '
                            error = 'The user has been generated successfully!'
                            session['activate_token'] = response['token']
                            if two_fa_auth_method == 'app':
                                redirectURL = "2fapp/qrcode/generate"
                            else:
                                redirectURL = "2fa/opt/send"
                                error = 'The user code has been generated successfully! Please check your email to activate your account.'
                            
                    else:
                        error = 'Failed to create user. Please try again later.'
                        redirectURL = "users/create"
                    
                    return jsonify({'message': error, 
                                            'status': status, "object": [], "redirectUrl": redirectURL,
                                            'secret': '',
                                            "otpqrcode": session['otpqrcode'],
                                            "otpqrcode_uri": 'static/otp_qrcode_images/' + str(session['otpqrcode'])
                                            }, url_status)            

            else:

                #create_user(db,firstname, lastname, email, country,country_code, phone, password_hash, session['user_secret_code'])

                """if len(two_factor_auth_code) != 6:
                    return jsonify({'message': 'Maximum digits required for the 2FA code is 6.', 'status': 'error', "redirectUrl": "users/create"}, 400)
                else:

                    OTP = request.form.get('two_factor_auth_code')
                    secret = request.form.get('secret')
                    
                    otpstatus = False
                    if OTP is not None and secret is not None:
                        otpstatus = verify_provisioning_uri(secret, OTP)

                        if otpstatus:
                            
                            try:
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
                            except Exception as e:
                                return jsonify({'message': 'Error: '+e, 'status': 'error', "redirectUrl": "users/create"}, 400) 
                        
                        else:
                            return jsonify({'message': '2FA OTP code is invalid.', 'status': 'error', "redirectUrl": "users/create"}, 400)
                    else:                 
                        return jsonify({'message': '2FA OTP code not found.', 'status': 'error', 'otpstatus':otpstatus, 
                                                "object": request.form, "redirectUrl": "users/create"}, 400)
                """
            
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

   
    
def capture_user_info():
    # Get User IP
    user_ip = request.remote_addr

    # Get User Mac Address
    user_mac = requests.get('https://api.macvendors.com').text

    # Get User Device Type
    user_agent = request.user_agent
    user_device = user_agent.platform

    return user_ip, user_mac, user_device