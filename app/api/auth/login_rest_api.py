
from flask import Blueprint, jsonify, request, current_app, make_response
from datetime import datetime
from flask.views import MethodView

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    current_user
)
from app.configs_package import jwt

from werkzeug.security import generate_password_hash, check_password_hash
from app.configs_package.modules.load_database import db
from flask_login import UserMixin

from app.api.auth.user_model import User
from app.api.auth.token_block_list import TokenBlocklist
from app.api.auth.refresh_token_view import RefreshToken

# Create a Blueprint for the API
login_rest_api_bp = Blueprint('jwt_api', __name__)


# Dummy User Database

class Userr(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    has_2fa = db.Column(db.Integer(), nullable=True, default=1)
    is_active = db.Column(db.Integer(), nullable=True, default=1)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    
# Login View to Get JWT Token
class LoginRestAPI(MethodView):
    def post(self):       

        if request.content_type != "application/json":
            return jsonify(error="Content-Type must be application/json"), 415
        
        data = request.get_json()
        if not data:
            return jsonify(error="Missing JSON body"), 400
        # Check if the username and password match
        #if users.get("username") != "admin" and users.get("password") != "password123":
        #    return jsonify(error="Invalid credentials", status_code=401), 401
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')    
    
        #user = User.query.filter_by(username=username).first()
        user=User().get_user_test()
        
        #if not user or not user.check_password(password):
        user_exists= True if user else False

        if username != user['username'] or not check_password_hash(user['password_hash'], password):
            return jsonify({"error": f"Invalid credentials {user['username']}"}), 201
        
        access_token = create_access_token(identity=str(user['id']))
        refresh_token = create_refresh_token(identity=str(user['id']))
        
        response = jsonify({
            "message": "Login successful",
            #"user": user.serialize(),
            "user": user,
            "status_code":200
        })
        
        

        # Create response and set `httpOnly` cookie
        response = make_response(response)
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)        
    
        #response.headers["Access-Control-Allow-Origin"] = "http://localhost:52330"
        #response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        #response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

        #token = create_access_token(identity=username)
        #        return jsonify(access_token=token)

from flask_jwt_extended import jwt_required, current_user
# Protected API View (Requires JWT)
class ProtectedAPI(MethodView):
    #decorators = [jwt_required()]
    @jwt_required()
    def get(self):
        return jsonify({
        "message": "Welcome to Protected data",
        "user": current_user.serialize()
    }), 200


# Register API Views
login_rest_api_bp.add_url_rule('/login', view_func=LoginRestAPI.as_view('login'))
login_rest_api_bp.add_url_rule('/protected', view_func=ProtectedAPI.as_view('protected'))
