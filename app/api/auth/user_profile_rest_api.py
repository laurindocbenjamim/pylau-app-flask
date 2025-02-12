
from flask import Blueprint, jsonify, request, current_app, make_response
from flask.views import MethodView
from app.api.auth.token_block_list import TokenBlocklist
from app.configs_package.modules.load_database import db
from app.api.auth.user_model import User
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, Sequence

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    current_user
)

user_profile_rest_api_bp=Blueprint('user_profile_api', __name__)

class UserProfileRestAPI(MethodView):
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        
        response = jsonify({"message": f"User profile {identity}"})
      
        return response
    
    #decorators = [jwt_required()]
    @jwt_required()
    def get(self):
        users=dict()
        error=None
        try:
            users = User.query.all()
        except SQLAlchemyError as e:
            error= str(e)
        except Exception as e:
            error= str(e)

        return jsonify({
        "message": "Welcome to the User Profile data",
        "user": current_user.serialize(),
        "error_get_users": error
    }), 200

# Register API Views
#refresh_token_bp.add_url_rule('/refresh', view_func=refresh)
user_profile_rest_api_bp.add_url_rule('/profile', view_func=UserProfileRestAPI.as_view('profile'))
