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
# Create a Blueprint for the API
jwt_api_blueprint = Blueprint('jwt_api', __name__)

# Dummy User Database

class User(db.Model, UserMixin):
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

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'
    
# Login View to Get JWT Token
class LoginJwtAPI(MethodView):
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
        return jsonify(error=f"I get the user {username}-{password}", status_code=200), 401
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Invalid credentials"}), 401
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        response = jsonify({
            "message": "Login successful",
            "user": user.serialize(),
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
        "message": "Protected data",
        "user": current_user.serialize()
    })

# Register API Views
jwt_api_blueprint.add_url_rule('/login', view_func=LoginJwtAPI.as_view('login'))
jwt_api_blueprint.add_url_rule('/protected', view_func=ProtectedAPI.as_view('protected'))
