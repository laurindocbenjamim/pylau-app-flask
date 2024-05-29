
from flask import Blueprint, request, jsonify, render_template
from core import db
from core import create_user, get_users, get_user_by_id, update_user, delete_user

bp = Blueprint('users', __name__, url_prefix='/users')    # Create a Blueprint object

@bp.route('/log', methods=['GET','POST'])   # Define a route for the login page
def loginuser():
    # Get the username and password from the request
    username = request.form.get('username')
    password = request.form.get('password')

    #user = create_user(db, username='faria', password='123')
    delete_user(db, id=8)
    users = get_users(db)
    #return render_template('index.html', people=all_people) 

    obj = update_user(db, username='Gamba', password='roooooooooot', id=1)

    
    return jsonify({'message': 'User created successfully', 'data': users, 'obj': obj})
    #return f"User logged in successfully: {user.username}"