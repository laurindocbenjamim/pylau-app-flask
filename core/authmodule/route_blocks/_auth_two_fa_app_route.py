

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


def route_two_fa_login(bp, db):
    @bp.route('/2fapp/login', methods=['GET', 'POST'])
    @cross_origin(methods=['GET', 'POST'])
    def two_fa_app_login():

        error = None
        status=None
        
        if session.get('token') is not None:
            return redirect(url_for('public_projects'))    

        if request.method == 'POST':
            code = request.form.get('otpcode')
            
            if g.user is None:
                error = 'User not identified.'
                flash(error)
                return render_template('auth/two_factor_app_auth.html', title='2FA-Authentication', status=status, message= error)                                       
            else:
                id = g.user['userID']

            if not code:
                status = 400 
                error = 'The 2-factor authentication code is required.'          

            elif id is not None:
                user = get_user_by_id(db,id)
                user = [] if user is None else user
                
                if len(user) == 0:
                    status = 400
                    error = 'Username not found.'
                    
                elif user['two_factor_auth_secret']:
                    if verify_provisioning_uri(user['two_factor_auth_secret'], code):
                        status = 0
                        error = 'Login successful.'
                        session.clear()
                        dataframe =  {
                            'email': user['email'],
                            'firstname': user['firstname'],
                            'lastname': user['lastname'],
                        }
                        session['user_logged'] = True
                        session['user_id'] = user['userID']
                        session['user_dataframe'] = dataframe 
                        token = generate_token(user['email'])
                        session['token'] = token 
                                
                        return redirect(url_for('public_projects'))
                                
                    else:
                        status = 1
                        error = 'The 2FA-code provided is invalid.'
                else:
                    status = 400
                    error = 'The 2FA-code not exists for this user.'
                    #abort(400)
                    return jsonify({'message': error, 'status': 'error', 'otpstatus': False, 
                                                "object": [], "redirectUrl": "auth/2fapp/login"}, 400)
                    
            flash(error)
            return render_template('auth/two_factor_app_auth.html', title='2FA-Authentication', status=status, message= error)
                                                            
            
        if request.method == 'GET':
            if g.user is not None:
                id = g.user['userID']
                return render_template('auth/two_factor_app_auth.html', title='2FA-Authentication', two_fa=True, status=0, message= 'ID: '+str(id)+' is logged in.')
            else:
                return redirect(url_for('Auth.signin'))
                #return jsonify({'message': 'Unauthorized access', 'status': 'error', 'otpstatus': False, 
                                #"object": [], "redirectUrl": "auth/2fapp/login"}, 400)
    

    # Load logged in user to verify if the user id is stored in a session
    @bp.before_app_request
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
    
