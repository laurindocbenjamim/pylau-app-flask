
import os
from flask import (
    Blueprint, render_template, url_for, request, redirect, jsonify
)

bpapp = Blueprint("Auth", __name__, url_prefix='/auth')

# Login function
@bpapp.route('/login', methods=['GET', 'POST'])
def login():
     
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         if username == 'admin' and password == 'admin':
             return redirect(url_for('dashboard'))
         else:
             return redirect(url_for('Auth.register'), 200, [{'Content-Type': 'application/json'}])
    if  request.method == 'GET':
        return render_template('auth/auth.html', title='Sign In')

# Register function
@bpapp.route('/register', methods=['GET', 'POST'])
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
            return jsonify({'Content-Type': 'application/json', "object": data, "redirectUrl": "2fa/google-get" }, 200)
    return render_template('auth/register.html', title='Sign Up')