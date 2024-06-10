
import flask
from ..model.users import Users
from .auth_register_view import AuthRegisterView


bp_auth_register_parent = flask.Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

# Initialize the application extension by passing the login_manager in the init_app function
def init_app():    
    bp_auth_register_parent.add_url_rule('/user/register', view_func=AuthRegisterView.as_view('register', Users, template='create_user.html'))

