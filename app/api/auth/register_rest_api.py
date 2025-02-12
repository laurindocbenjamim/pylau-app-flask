
from flask import Blueprint, jsonify, request, current_app, make_response
from datetime import datetime
from flask.views import MethodView

from app.configs_package.modules.load_database import db
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.auth.user_model import User


# Create a Blueprint for the API
register_rest_api_bp = Blueprint('register_api', __name__)

# Login View to Get JWT Token
class ResgiterRestAPI(MethodView):
    def post(self):  
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully"}), 201

# Register API Views
register_rest_api_bp.add_url_rule('/register', view_func=ResgiterRestAPI.as_view('register'))

    