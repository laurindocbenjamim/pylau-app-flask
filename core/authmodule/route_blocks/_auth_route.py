

import os
import functools

from flask import (
    render_template, g, url_for, request, redirect, jsonify, abort, session, flash
)
from werkzeug.security import check_password_hash

from flask_cors import cross_origin
from core.config import verify_provisioning_uri
from core import get_user_by_email, get_user_by_id, get_user_by_id_limited_dict
from core.config import token_required, generate_token, decode_token, token_required
from functools import wraps


def route_auth(bp, db):
    @bp.route('/login', methods=['GET', 'POST'])
    @cross_origin(methods=['GET', 'POST'])
    def signin():

        error = None
        status=None
        
        if session.get('token') is not None:
            return redirect(url_for('public_projects'))    

        if request.method == 'POST':
            email = request.form.get('username')
            password = request.form.get('password')

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
                    else:
                        session.clear()
                        g.user = user
                        session['user_id'] = user['userID']
                        session['firstname'] = user['firstname']
                        session['lastname'] = user['lastname']
                        #session['secret'] = user['two_factor_auth_secret']
                        session['email'] = user['email']
                        session['user_status'] = user['status']
                        return redirect(url_for('Auth.two_fa_app_login'))
                        #return jsonify({'message': 'User is ready to be created successfully!', 'status': 3, 'otpstatus':None, 
                                        #"object": g.user, "redirectUrl": "2fapp/qrcode/get"}, 200)
                       
            flash(error)
            return render_template('auth/auth.html', title='Sign In', status=status, message= error)
                                                            
            
        if request.method == 'GET':
            return render_template('auth/auth.html', title='Sign In', two_fa=True, status=0, message= '')
    

    """
    # Load logged in user to verify if the user id is stored in a session
    @bp.before_app_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = get_user_by_id_limited_dict(db,user_id) 

    
    # REQUIRE A UTHENTICATION IN OTHER VIEWS 
    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('Auth.two_fa_app_login'))

            return view(**kwargs)

        return wrapped_view
    """
    
