
import functools
from datetime import date, datetime, timedelta


from flask import (
    Blueprint,request,jsonify,session,g, render_template, redirect, url_for,
    flash
    
)
from markupsafe import escape
from flask_cors import CORS, cross_origin
from core import db
from core import get_token_by_token
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
@bp.route('/activate/<string:token>', methods=['GET'])    # Define a route for the login page
@cross_origin(methods=['GET'])
def activate_user_account(token):
    
    if token is None:
        #return jsonify([{'message': 'Token is required', 'data': []}])
        error = 'Token is required'
    else:
        session.clear()
        user_token = get_token_by_token(escape(token))
        
        if user_token is None:
            flash('Token has not found', 'error')
            return redirect(url_for('Users.sign_up'))
        elif len(user_token) == 0:
            flash('Token has not found. Maybe not registered', 'danger')
            #return redirect(url_for('Users.sign_up'))
            return jsonify([{'message': 'Token is required', 'data': [user_token, escape(token)]}])
        else:
            
            user = [user for user in user_token][0]
            user_id = user['userID']
            u_token = user['token']

            if u_token != escape(token):
                flash('Invalid token detected', 'danger')
                return redirect(url_for('Users.sign_up'))
            
            created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#user['created_date']
            created_date = datetime.strftime(user['created_date'],'%Y-%m-%d %H:%M:%S')            
            date_obj = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
            date_created_int = int(date_obj.timestamp())
            
            date_now_int = int(datetime.now().timestamp())
            expire_time = user['expire_time']
            
            #date_obj = datetime.strptime(str(created_date), '%a, %d %b %Y %H:%M:%S %Z')
            

            expiration_date = date_obj + timedelta(days=expire_time)

            time_remaining = expiration_date - datetime.now()
            #time_remaining_int = int(datetime.strptime(str(time_remaining), '%Y-%m-%d %H:%M:%S').timestamp())
            total_seconds = int(time_remaining.total_seconds())
            total_minutes = total_seconds // 60
            total_hours = total_minutes // 60
            time_left_days = total_hours // 24
            
            if total_seconds == 0:
                flash('Token has expired', 'danger')
                return render_template('auth/success_registration.html', title="Expired token")
            else:
                resp = update_user_status(db, user_id, 'active')
                
                if resp is not None:
                    #return jsonify([{'message': 'User found', 'data': resp['email']}])
                    return redirect(url_for('Auth.signin'))
    flash('Token has not found', 'danger')
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

    if 'firstname' and 'lastname' not in session:
        flash('Failed to create user', 'error')
        return redirect(url_for('Auth.signin'))                
    elif 'lastname' not in session:
        flash('Failed to create user', 'error')
        return redirect(url_for('Auth.signin'))       
    else:
        flash('User created successfully', 'success')
        return render_template('auth/success_registration.html', title="User created successfull", firstname=session['firstname'], 
                           lastname=session['lastname'])
    
    
   

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

    


