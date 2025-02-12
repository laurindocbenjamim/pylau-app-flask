
from datetime import datetime
from flask import Blueprint, jsonify, request, current_app, make_response
from flask.views import MethodView
from app.api.auth.token_block_list import TokenBlocklist
from app.configs_package.modules.load_database import db

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

refresh_token_bp=Blueprint('refresh_token', __name__)

class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            jti = get_jwt()["jti"]

            # Revoke old refresh token
            db.session.add(TokenBlocklist(
                jti=jti,
                token_type="refresh",
                user_id=current_user,
                expires=datetime.utcfromtimestamp(get_jwt()["exp"])
            ))
            
            # Create new tokens
            new_access = create_access_token(identity=current_user)
            new_refresh = create_refresh_token(identity=current_user)

            response = jsonify({
                "message": "Tokens refreshed",
                "access_token": new_access,
                "refresh_token": new_refresh
            })
            
            set_access_cookies(response, new_access)
            set_refresh_cookies(response, new_refresh)
            
            db.session.commit()
            return response

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
# Create routes
#@refresh_token_bp.route('/refresh', methods=['POST'])
#@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    response = jsonify({"message": "Token refreshed"}), 200
    set_access_cookies(response, access_token)
    return response

# Register API Views
#refresh_token_bp.add_url_rule('/refresh', view_func=refresh)
refresh_token_bp.add_url_rule('/refresh', view_func=RefreshToken.as_view('refresh'))
