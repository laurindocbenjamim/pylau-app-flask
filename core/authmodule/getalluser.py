from flask import jsonify
from flask_cors import CORS, cross_origin
from core import get_users
def get_allusers(bpapp, db):
    @bpapp.route('/getall', methods=['GET'])    # Define a route for the login page
    @cross_origin(methods=['GET'])
    def get_allusers():
        users = get_users(db)
        
        return jsonify({'message': 'Users found', 'data': users})
        #return f"User logged in successfully: {user.username}"