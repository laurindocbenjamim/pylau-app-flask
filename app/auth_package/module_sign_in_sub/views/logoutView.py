from flask.views import View   
from flask import session,redirect, url_for, request, flash,jsonify
from flask_login import login_required, logout_user
from markupsafe import escape

class LogoutView(View):
    methods = ['GET']
    decorators = [login_required]

    def __init__(self, userToken, authUserHistoric):
        self.userToken = userToken
        self.authUserHistoric = authUserHistoric

    def dispatch_request(self, user_token=None):
        session.pop('_flashes', None)
        if user_token:

            # Check if the token is expired
            if self.userToken.is_user_token_expired(escape(user_token)):
                session.clear()
                logout_user()
                return [user_token]
            else:
                # Update the user's historic data
                status, token = self.userToken.get_token_by_token(escape(user_token))
                return [status, token]
                if status and token:                    
                    #self.userToken.expire_the_user_token_by_user(token.username, token.token)
                    status, exp_token = self.userToken.force_user_jwt_token_expiration(user_token)
                    session['user_token'] = ''

                    self.authUserHistoric.update_auth_user(0, token.username, False)                    
                    #resp, exp_token = self.userToken.force_user_jwt_token_expiration(token.token)    
                #return jsonify({"sms": exp_token})
                logout_user()
                session.clear()
                session.pop('user_id', None)
                session.pop('username', None)
                session.pop('user_token', None)
                session.pop('email', None)
        else:
            status, obj = self.authUserHistoric.update_auth_user(session.get('user_id'), session.get('email'), False)
            #re, obj2 = self.userToken.expire_the_user_token_by_user(session.get('email'), session.get('user_token'))
            status, exp_token = self.userToken.force_user_jwt_token_expiration(user_token)
            session['user_token'] = ''
            logout_user()
            session.clear()
            session.pop('user_id', None)
            session.pop('username', None)
            session.pop('user_token', None)
            session.pop('email', None)
            #return jsonify({'message': 'User token is required'}), 400
        return redirect(url_for('auth.user.login'))