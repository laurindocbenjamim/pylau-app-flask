
"""
To use this module you need to install the following libraries:
pip install pyjwt
"""
import jwt
import json
import requests
from flask import Flask, Request
from .logger_config import get_message as set_logger_message

from datetime import datetime, timedelta, timezone
from flask import request, jsonify, current_app
from functools import wraps

"""
This method is used to cover the route in order to 
veriy is the user who are requiring the route acess have 
or not an acess token
"""
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        """
        This method is used to cover the route in order to 
        veriy is the user who are requiring the route acess have 
        or not an acess token
        """
        token = request.headers["Authorization"]
        token = str.replace(str(token), 'Bearer ', '')
        token = str(token).replace(" ", "")        
        #token = requests.get('token').json()
        if not token:
            return jsonify({'Alert!': 'Token is missing!', "token": token}, 401)        
        try:
            #payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=10, algorithms="HS256")
            return payload
        except jwt.ExpiredSignatureError as e:
            error = f"{e}"
            set_logger_message(f"JWT <<decorated method>> ExpiredSignatureError: {str(e)}")
            return jsonify({"error": error},401)
    return decorated

def decode_token(token):    
    token = str.replace(str(token), 'Bearer ', '')
    token = str(token).replace(" ", "")        
    #token = requests.get('token').json()
    if not token:
        return jsonify({'Alert!': 'Token is missing!', "token": token}, 401)        
    try:
        #payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=10, algorithms="HS256")
        payload["status_code"] = 200
        return payload
    except jwt.ExpiredSignatureError as e:
        error = f"{e}"
        set_logger_message(f"JWT <<decode_token method>> ExpiredSignatureError: {str(e)}")
        return {"error": error, "status_code": 401}

"""  This method generate a token using the JWT library """
def generate_token(user):

    token = None
    date_serialized = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
    secret_key = current_app.config['SECRET_KEY']

    payload = {
        "user": str(user), 
        'exp': date_serialized, 
        "nbf": datetime.now(tz=timezone.utc) 
        }
    
    try:
        #date = datetime.now() + timedelta(seconds=1800) # 1800 seconds is equal 30 minutes
        #date_serialized = json.dumps(date, default=str)          

        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token
    except Exception as e:
        set_logger_message(f"JWT <<generate_token method>> ExpiredSignatureError: {str(e)}")
    return None

def refresh_jwt_token(token):
    secret_key = current_app.config['SECRET_KEY']
    new_token = None
    try:
        set_logger_message(f"<<refresh_jwt_token method>> START TO TRY TO DECODE TOKEN")
        # First try to decode the token. If it's expired it will raise an exception
        jwt.decode(token, secret_key, algorithms="HS256")  

    except jwt.ExpiredSignatureError as e:     

        set_logger_message(f"JWT <<refresh_jwt_token method>> ExpiredSignatureError: {str(e)}")
        # If the token is expired generate a new one
        set_logger_message(f"<<refresh_jwt_token method>> START TRYING TO REFRESH THE TOKEN")

        try:
            set_logger_message(f"<<refresh_jwt_token method>> START TRYING TO DECODE THE TOKEN")

            user = jwt.decode(token, secret_key, leeway=10, algorithms="HS256", options={'verify_exp': False})['user']

            set_logger_message(f"<<refresh_jwt_token method>> START TRYING TO REFRESH THE TOKEN")

            new_token = generate_token(user)

            set_logger_message(f"<<refresh_jwt_token method>> THE TOKEN HAS BEEN REFRESHED [!]")

            return True, new_token
        except Exception as ex:

            set_logger_message(f"JWT <<refresh_jwt_token method>> ExpiredSignatureError -> [Exception]: {str(ex)}")

            return False, None
    except Exception as e:

        set_logger_message(f"JWT <<refresh_jwt_token method>> Exception: {str(e)}")

        return False, None
    else:
        return True, token

def is_user_token_expired(token):
    secret_key = current_app.config['SECRET_KEY'] 

    if not token or '':
        return None        
    try:
        response = jwt.decode(token, secret_key, leeway=10, algorithms="HS256", options={'verify_exp': True})['user']
        return False
    except jwt.ExpiredSignatureError as e:
        set_logger_message(f"JWT <<decode_token method>> ExpiredSignatureError: {str(e)}")
        return True
    
def filter_token_from_headers(headers):
    token = headers["Authorization"]
    token = str.replace(str(token), 'Bearer ', '')
    return token
    