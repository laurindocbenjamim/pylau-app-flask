
import os

from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify, abort, session, flash
)
from werkzeug.security import check_password_hash

from flask_cors import CORS, cross_origin
from core.config import verify_provisioning_uri
from core import get_user_by_email, check_email_exists
from core import db

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
     
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        code = request.form.get('otpcode')
        error = None
        if email == '':
             
            return render_template('auth/auth.html', title='Sign In', status=400, message= 'Email is required.')
            #return jsonify({'message': 'Email is required.', 'status': 'error', 'otpstatus': False, 
            #                                "object": [], "redirectUrl": "auth/2fapp/login"}, 400)
        if password == '':
            error = 'Password is required.'
            abort(400)
            
        
        if email != '' and password != '':
            user = get_user_by_email(email)
            user = [] if user is None else user
            
            if user is None:
                error = 'Usernam not found.'
                abort(400)
                
            else:
                
                if check_password_hash(user['password'], password) == False:
                    error = 'Password is wrong.'
                    abort(400)
                                    
                if code == '':
                    error = 'Enter the code provided by your auth app.'
                    abort(400) 
                else:
                    if user['two_factor_auth_secret']:
                        if verify_provisioning_uri(user['two_factor_auth_secret'], code):
                            return jsonify({'message': 'User logged successfull.', 'status': 1, 'otpstatus': True, 
                                                "object": user, "redirectUrl": "dashboard"}, 200)
                        else:
                            error = 'The 2FA-code is invalid.'
                            abort(400)
                    else:
                        error = 'The 2FA-code not exists for this user.'
                        abort(400)
        flash(error)
        return render_template('auth/auth.html', title='Sign In', status=400, message=error)
                                                        
        
    if request.method == 'GET':
        return render_template('auth/auth.html', title='Sign In', two_fa=True)

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
