from flask import jsonify
from flask_cors import cross_origin
from core.authmodule.UserController import get_users
def get_all_users(bp, db):
    @bp.route('/get-all', methods=['GET'])    # Define a route for the login page
    @cross_origin(methods=['GET'])
    def get_allusers():
        users = get_users(db)
        dataframe = []
        for user in users:
            
            dataframe.append({
                'userID': user['userID'],
                'email': user['email'],
                'firstname': user['firstname'],
                'lastname': user['lastname'],
                'country': user['country'],
                'phone': user['phone'],
                'country_code': user['country_code'],
                'date_added': user['date_added'],
                'date_updated': user['date_updated']
            })
        return jsonify({'message': 'Users found', 'object': dataframe})
        #return f"User logged in successfully: {user.username}"