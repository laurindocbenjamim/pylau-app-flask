from flask.views import View   
from flask import session,redirect, url_for, request, flash,jsonify
from flask_login import login_required, logout_user

class LogoutView(View):
    methods = ['GET']
    decorators = [login_required]

    def __init__(self, userToken):
        self.userToken = userToken

    def dispatch_request(self, user_token=None):
        if user_token:
            user_token = user_token
            logout_user()
            session.clear()
        else:
            return jsonify({'message': 'User token is required'}), 400
        return redirect(url_for('auth.user.login'))