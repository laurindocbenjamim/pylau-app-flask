

import os
import functools

from flask import (
    render_template, g, url_for, request, redirect, jsonify, abort, session, flash
)
from werkzeug.security import check_password_hash

from flask_cors import cross_origin
from core.config import verify_provisioning_uri
from core import get_user_by_email, get_user_by_id
from core.config import token_required, generate_token, decode_token, token_required
from functools import wraps


def route_two_fa_login(bpapp, db):
    @bpapp.route('/2fapp/login', methods=['GET', 'POST'])
    @cross_origin(methods=['GET', 'POST'])
    def two_fa_app_login():

        error = None
        status=None
        
        if session.get('token') is not None:
            return redirect(url_for('public_projects'))    

        if request.method == 'POST':
            email = request.form.get('username')
            password = request.form.get('password')
            code = request.form.get('otpcode')

            if not email:
                status = 400 
                error = 'Email is required.'
            if not password:
                status = 400
                error = 'Password is required.'            
            
            if email and password != '':
                user = get_user_by_email(email)
                user = [] if user is None else user
                
                if len(user) == 0:
                    status = 400
                    error = 'Username not found.'
                    
                else:
                    
                    if check_password_hash(user['password'], password) == False:
                        status = 400
                        error = 'Password is wrong.'

                    elif code == '':
                        error = 'Enter the code provided by your auth app.'
                        status = 1
                    else:
                        if user['two_factor_auth_secret']:
                            if verify_provisioning_uri(user['two_factor_auth_secret'], code):
                                status = 0
                                error = 'Login successful.'
                                session.clear()
                                dataframe =  {
                                    'userID': user['userID'],
                                    'email': user['email'],
                                    'firstname': user['firstname'],
                                    'lastname': user['lastname'],
                                    'country': user['country'],
                                    'phone': user['phone'],
                                    'country_code': user['country_code'],
                                    'date_added': user['date_added'],
                                    'date_updated': user['date_updated'],
                                }
                                session['user_logged'] = True
                                session['user_id'] = user['userID']
                                session['user_dataframe'] = dataframe 
                                token = generate_token(user['email'])
                                session['token'] = token 
                                
                                return redirect(url_for('public_projects'))
                                
                            else:
                                status = 1
                                error = 'The 2FA-code is invalid.'
                        else:
                            status = 400
                            error = 'The 2FA-code not exists for this user.'
                            #abort(400)
                            #return jsonify({'message': error, 'status': 'error', 'otpstatus': False, 
                                                #"object": [], "redirectUrl": "auth/2fapp/login"}, 400)
            flash(error)
            return render_template('auth/auth.html', title='Sign In', status=status, message= error)
                                                            
            
        if request.method == 'GET':
            return render_template('auth/auth.html', title='Sign In', two_fa=True, status=0, message= '')
    

    # Load logged in user to verify if the user id is stored in a session
    @bpapp.before_app_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = get_user_by_id(db,user_id) 

    
    # REQUIRE A UTHENTICATION IN OTHER VIEWS 
    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('Auth.two_fa_app_login'))

            return view(**kwargs)

        return wrapped_view
    
