from flask.views import View   
from flask import session,redirect, url_for, request, flash,jsonify
from flask_login import login_required, logout_user

class LogoutView(View):
    methods = ['GET']
    decorators = [login_required]

    def __init__(self, userToken, authUserHistoric):
        self.userToken = userToken
        self.authUserHistoric = authUserHistoric

    def dispatch_request(self, user_token=None):
        if user_token:
            # Update the user's historic data
            status, token = self.userToken.get_token_by_token(user_token)
            if status and token:
                self.authUserHistoric.update_auth_user(0, token.username, False)
                
            logout_user()
            session.clear()
            session.pop('username', None)
            session.pop('user_token', None)
            session.pop('username', None)
        else:
            return jsonify({'message': 'User token is required'}), 400
        return redirect(url_for('auth.user.login'))