

from datetime import date

from flask import (
    Blueprint,request,jsonify,
    
)
from markupsafe import escape
from flask_cors import CORS, cross_origin
from core import db
from core import (get_users, 
                  get_user_by_id, get_user_by_email, 
                  update_user, delete_user
                  )

bp = Blueprint('Users', __name__, url_prefix='/users')    # Create a Blueprint object
CORS(bp)

# Importing the route blocks
from core.authmodule.route_blocks._user_get_all_route import get_all_users
from core.authmodule.route_blocks._user_create_route import create_new_user

# Loading block of routes
create_new_user(bp, db)
get_all_users(bp, db)


# get user by id
@bp.route('/<int:userid>/get', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def getuser_by_id(userid):
    users = get_user_by_id(db, escape(userid))
    
    return jsonify([{'message': 'User found', 'data': users}])
    #return f"User logged in successfully: {user.username}"

@bp.route('/get/<string:email>', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def getuser_by_email(email=None):
    users = get_user_by_email(escape(email))
    
    return jsonify([{'message': 'User found', 'data': escape(email)}])


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
@bp.route('/<int:userid>/delete', methods=['GET'])    #
@cross_origin(methods=['GET'])
def deleteuser(userid):
    
    delete_user(db, userid)
    users = get_users(db)
    return jsonify([{'message': 'User deleted successfully', 'data': users}])



    


