
import os

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify, abort, session, flash
)
from werkzeug.security import check_password_hash

from flask_cors import CORS, cross_origin
from core.config import verify_provisioning_uri
from core import get_user_by_email, check_email_exists
from core import db
from core.config import token_required, generate_token, decode_token, token_required
from functools import wraps

bpapp = Blueprint("Auth", __name__, url_prefix='/auth')
CORS(bpapp)

# Login function
@bpapp.route('/login', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def login():
     
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin' and password == 'admin':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('Auth.register'), 200, [{'Content-Type': 'application/json'}])
    if  request.method == 'GET':
        return render_template('auth/auth.html', title='Sign In')
    

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

        if email == '':
            status = 400 
            error = 'Email is required.'
        if password == '':
            status = 400
            error = 'Password is required.'            
        
        if email != '' and password != '':
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

def two_fa_login():
     
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin' and password == 'admin':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('Auth.register'), 200, [{'Content-Type': 'application/json'}])
    if  request.method == 'GET':
        return render_template('auth/auth.html', title='Sign In')
    
# Register function
@bpapp.route('/register', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        country = request.form['country']
        countrycode = request.form['countrycode']
        phone = request.form['phone']

        data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'password': password,
            'confirm': confirm,
            'country': country,
            'countrycode': countrycode,
            'phone': phone
        }
        if email == 'rocketmc2009@gmail.com' and password == 'admin':
            return jsonify({'Content-Type': 'application/json', "object": data, "redirectUrl": "2fapp/verify" }, 200)
        else:
            return jsonify({"object": data, "redirectUrl": "auth/register" }, 200)
    return render_template('auth/register.html', title='Sign Up')


@bpapp.route('/logout', methods=['GET'])
@cross_origin(methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('Auth.two_fa_app_login'))