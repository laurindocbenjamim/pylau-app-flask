import flask

from .authViews.authView import AuthView

from flask_login import LoginManager



bp = flask.Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

def init_app(login_manager, db):
    
    from ..model.users import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)
       
    
    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('username')
        users = [user.to_dict() for user in Users.query.all()]
        user = [u for u in users if u['email'] == email]
        if not user:
            return
        user = user[0]
        #user.id = email
        return user
    
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return 'Unauthorized', 401

    bp.add_url_rule('/login', view_func=AuthView.as_view('login', Users,  template='auth.html'))

