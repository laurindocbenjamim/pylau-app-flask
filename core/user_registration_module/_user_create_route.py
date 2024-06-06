
import functools

import re
import requests

from datetime import date
from flask import jsonify, g, session, request, render_template, redirect, url_for, flash
from flask_cors import cross_origin
from core import (
    validate_form_fields, is_valid_email,
    check_email_exists, check_phone_exists, create_user,
    generate_token
)

from core import create_token
from werkzeug.security import check_password_hash, generate_password_hash
from core.config import generate_secret


def _create_new_user(bp, db):
    @bp.route('/user/create', methods=['GET', 'POST'])   # Define a route for the login page
    @cross_origin(methods=['GET', 'POST'])
    def sign_up():

        title='Sign Up'
        error = ''
        redirectURL = 'register/user/create'
        url_status = 400
        error_type = 'error'
        status = ''
        otpqrcode_uri = ''
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
                return jsonify({'message': 'The 2FA auth method is required.', 'status': 'error', "redirectUrl": redirectURL}, url_status)
            
            # validate the fields
            validate_form_fields(firstname, lastname, email, country,
                country_code, phone, password, confirm, '123456')
            
            # check if email is valid
            if is_valid_email(email) == False:
                return jsonify({'message': 'Invalid email address. Accepted emails: gmail.com, outlook.com, hotmail.com, live.com, icloud.com', 'status': 'error', "redirectUrl": redirectURL}, 400)
            
            # check if email exists
            if check_email_exists(email):
                return jsonify({'message': 'Email already exists', 'status': 'error', "redirectUrl": redirectURL}, url_status)
            
            # check if phone exists
            if check_phone_exists(phone):
                return jsonify({'message': 'Phone already exists', 'status': 'error', "redirectUrl": redirectURL}, url_status)
            
            # hash the password
            password_hash = generate_password_hash(password)

            if not check_password_hash(password_hash, confirm):
                return jsonify({'message': 'The passwords do not match', 'status': 'error', "object": [], "redirectUrl": redirectURL}, url_status)

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
                            url_status = 400                            
                        else:
                            url_status = 200
                            status = 2
                            error = 'User created successfully!: '
                            error = 'The user has been generated successfully!'
                            session['activate_token'] = response['token']
                            if two_fa_auth_method == 'app':
                                redirectURL = "register/qrcode/generate"
                            else:
                                redirectURL = "register/send/opt/email"
                                error = 'The user code has been generated successfully! Please check your email to activate your account.'
                            
                    else:
                        error = 'Failed to create user. Please try again later.'
                        redirectURL = "register/user/create"
                        status = 'error'
                        url_status = 400
                        otpqrcode_uri = 'static/otp_qrcode_images/' + str(session['otpqrcode'])
                    
                    return jsonify({'message': error, 
                        'status': status, "object": [], "redirectUrl": redirectURL,
                        'secret': '', "otpqrcode": session['otpqrcode'], 
                        "otpqrcode_uri": 'static/otp_qrcode_images/' + str(session['otpqrcode']) }, 
                        url_status)    
                                                    

            

        flash(error, error_type)   
           
        return render_template('auth/register.html', title='Sign Up')
        #return jsonify({'title': title,'message': error, 'status': status, "object": [], "redirectUrl": redirectURL,
                #'secret': '',"otpqrcode": session['otpqrcode'], 
                #"otpqrcode_uri": otpqrcode_uri }, url_status)     

   
    
