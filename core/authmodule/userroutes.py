
import functools
from datetime import date

from flask import (
    Blueprint,request,jsonify,session,g, render_template, redirect, url_for
    
)
from markupsafe import escape
from flask_cors import CORS, cross_origin
from core import db
from core import (get_users, 
                  get_user_by_id, get_user_by_email, 
                  update_user, update_user_status, delete_user
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

# get user by id
@bp.route('/activate/<int:userid>', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def activate_user_account(userid):
    try:
        #users = get_user_by_id(db, escape(userid))
        resp = update_user_status(db, escape(userid), 'active')

        if resp is not None:
            #return jsonify([{'message': 'User found', 'data': resp['email']}])
            return redirect(url_for('Auth.signin'))
    except Exception as e:
        #return jsonify([{'message': 'User not found ', 'data': []}])
        return render_template('errors/generic.html', title="Activate Account", 
                               message="Account activation failed. "+type(e).__name__, status=0)
    
    return redirect(url_for('Users.sign_up'))

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

@bp.route('/created', methods=['GET', 'POST'])
def success_registration():

    if session['firstname'] and session['lastname'] is not None:
        return render_template('auth/success_registration.html', title="User created successfull", firstname=session['firstname'], 
                           lastname=session['lastname'])
    return redirect(url_for('Auth.signin'))
   

 # Load logged in user to verify if the user id is stored in a session
@bp.before_app_request
def load_created_in_user():
    email = session.get('email')

    if email is None:
        g.user = None
    else:
        g.user = {'email': email}
    
# REQUIRE A UTHENTICATION IN OTHER VIEWS 

def login_not_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            #return redirect(url_for('Auth.signin'))
            return jsonify({'message': 'User is ready to be created successfully!', 'status': 3, 'otpstatus':None, 
                                                "object": [], "redirectUrl": "2fapp/qrcode/get"}, 200)

        return view(**kwargs)

    return wrapped_view

    


