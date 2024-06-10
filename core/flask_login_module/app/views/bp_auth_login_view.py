import flask
from flask import render_template

from .authLoginView.auth_login_view import AuthLoginView

from flask_login import logout_user, login_user



bp_auth_login_child = flask.Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

def init_app(login_manager, db):
    
    from ..model.users import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)
       
    
    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('username')
        """users = [user.to_dict() for user in Users.query.all()]
        user = [u for u in users if u['email'] == email]
        if not user:
            return

        """
        user = Users.query.get(email)
        if user.is_active() == False:
            # Use the login_user method to log in the user
            login_user(user)
            return flask.redirect(flask.url_for('select.user_list_view'))  
        # user = user[0]
        #user.id = email
        return user
    
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        #return 'Unauthorized', 401
        return flask.redirect(flask.url_for('auth.user.login'))

    bp_auth_login_child.add_url_rule('/login', view_func=AuthLoginView.as_view('login', Users,  template='auth.html'))

    # Logout route
    @bp_auth_login_child.route('/logout')
    def logout():
        #flask.session.clear()
        logout_user()
        return flask.redirect(flask.url_for('auth.user.login'))

