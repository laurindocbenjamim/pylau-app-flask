
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

logout_rest_api_bp=Blueprint('logout_rest_api', __name__)

class LogoutRestAPI(MethodView):
    @jwt_required()
    def post(self):
        # Revoke current tokens
        access_jti = get_jwt()["jti"]
        refresh_jti = get_jwt().get("refresh_jti")
        
        db.session.add_all([
            TokenBlocklist(
                jti=access_jti,
                token_type="access",
                user_id=current_user.id,
                expires=get_jwt()["exp"]
            ),
            TokenBlocklist(
                jti=refresh_jti,
                token_type="refresh",
                user_id=current_user.id,
                expires=get_jwt()["exp"]
            ) if refresh_jti else None
        ])
        db.session.commit()
        
        response = jsonify({"message": "Logged out"})
        unset_jwt_cookies(response)
        return response
    
# Create routes
#@logout_rest_api_bp.route('/logout', methods=['POST'])
#@jwt_required(refresh=True)
def logout():
    identity = get_jwt_identity()
    #access_token = create_access_token(identity=identity)
    #response = jsonify({"message": "Logout"})
    #set_access_cookies(response, access_token)
    response=jsonify({"message": f'Logouting Identity {identity}'}), 400
    return response

# Register API Views
#logout_rest_api_bp.add_url_rule('/refresh', view_func=refresh)
logout_rest_api_bp.add_url_rule('/logout', view_func=LogoutRestAPI.as_view('logout_rest_api'))
