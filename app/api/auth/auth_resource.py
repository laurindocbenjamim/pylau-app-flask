from app.dependencies import request, current_app, jsonify, Resource

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from app.api.auth.factory import sanitize_input


from app import csrf_global
from app.api.auth.user_model import User

#@csrf_global.exempt # This Exclude views from protection
class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        email = sanitize_input(data.get('email'))
        password = sanitize_input(data.get('password'))
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify(error="Invalid credentials"), 401
        
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    def get(self):
        return jsonify({"message": "Get something"})