import flask
from flask import render_template, jsonify

from .auth_login_view import AuthLoginView
from ...token_module.userTokenModel import UserToken
from ...two_factor_auth_module.twoFAModel import TwoFAModel

from flask_login import logout_user, login_user



bp_auth = flask.Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

def init_app(login_manager, db):
    
    from ...user_module import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)
       
    
    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('username')
        
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.is_active() == True:
                # Use the login_user method to log in the user                
                return flask.redirect(flask.url_for('projects.list'))   
        return 
    
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        #return 'Unauthorized', 401
        return flask.redirect(flask.url_for('auth.user.login'))

    bp_auth.add_url_rule('/login', view_func=AuthLoginView.as_view('login', Users, UserToken, TwoFAModel,  template='auth/auth.html'))

    # Logout route
    @bp_auth.route('/logout')
    def logout():
        flask.session.clear()
        logout_user()
        return flask.redirect(flask.url_for('auth.user.login'))

