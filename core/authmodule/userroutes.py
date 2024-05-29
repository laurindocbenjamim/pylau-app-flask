
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, make_response, request, session, url_for,jsonify,
    abort
)
from flask_cors import CORS, cross_origin
from core import db
from core import create_user, get_users, get_user_by_id, update_user, delete_user

bp = Blueprint('users', __name__, url_prefix='/users')    # Create a Blueprint object
CORS(bp)

@bp.route('/create', methods=['GET', 'POST'])   # Define a route for the login page
@cross_origin(methods=['GET', 'POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')

    user = create_user(db, username, password)
    users = get_users(db)
    return jsonify({'message': 'User created successfully', 'user': user, 'data': users})

# get all users
@bp.route('/get-all', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def get_all_users():
    users = get_users(db)
    
    return jsonify({'message': 'Users found', 'data': users})
    #return f"User logged in successfully: {user.username}"

# get user by id
@bp.route('/<userid>/get', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def getuser_by_id(userid):
    users = get_user_by_id(db, userid)
    
    return jsonify([{'message': 'User found', 'data': users}])
    #return f"User logged in successfully: {user.username}"


# Update user
@bp.route('/update', methods=['POST'])    # 
@cross_origin(methods=['POST'])
def update_user():
    username = request.form.get('username')
    password = request.form.get('password')
    id = request.form.get('id')

    obj = update_user(db, 'Gamba', 'roooooooooot', 1)

    users = get_users(db)
    return jsonify([{'message': 'User updated successfully', 'data': users}])

# Delete a usergit 
@bp.route('/<userid>/delete', methods=['GET'])    #
@cross_origin(methods=['GET'])
def deleteuser(userid):
    
    delete_user(db, userid)
    users = get_users(db)
    return jsonify([{'message': 'User deleted successfully', 'data': users}])