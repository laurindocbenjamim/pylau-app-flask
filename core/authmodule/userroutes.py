
from flask import Blueprint, request, jsonify, render_template
from core import db
from core import create_user, get_users, get_user_by_id

bp = Blueprint('users', __name__, url_prefix='/users')    # Create a Blueprint object

@bp.route('/log', methods=['GET','POST'])   # Define a route for the login page
def loginuser():
    # Get the username and password from the request
    username = request.form.get('username')
    password = request.form.get('password')

    user = create_user(db, username='faria', password='123')
    
    #all_people = get_all_people(db)
    #return render_template('index.html', people=all_people) 
    #return jsonify({'message': 'User logged in successfully', 'data': user})
    return f"User logged in successfully: {user.username}"