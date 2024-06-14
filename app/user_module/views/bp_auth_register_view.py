
import flask
from ..model.users import Users
from ...token_module.userTokenModel import UserToken
from .authRegisterView import AuthRegisterView
from .activateAccountView import ActivateAccountView


bp_auth_register_parent = flask.Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

# Initialize the application extension by passing the login_manager in the init_app function
def init_app():    
    bp_auth_register_parent.add_url_rule('/user/register',\
                                          view_func=AuthRegisterView.as_view('register', Users, UserToken, template='auth/create_user.html'))
    bp_auth_register_parent.add_url_rule('/user/activate/account/<string:token>',\
                                          view_func=ActivateAccountView.as_view('activate_account', Users, UserToken, template='auth/create_user.html'))

