
import flask
from flask_cors import CORS
from ..model.users import Users
from ....token_module.userTokenModel import UserToken
from .authRegisterView import AuthRegisterView
from .activateAccountView import ActivateAccountView
from ....two_factor_auth_module.twoFAModel import TwoFAModel
from ...module_recover_accout.bp_account_recovery import bp_acc_recover


bp_auth_register_parent = flask.Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')
CORS(bp_auth_register_parent)
# Initialize the application extension by passing the login_manager in the init_app function
def init_register_app():    
    bp_auth_register_parent.add_url_rule('/user/register',\
                                          view_func=AuthRegisterView.as_view('register', Users, UserToken, TwoFAModel, template='auth/create_user.html'))
    bp_auth_register_parent.add_url_rule('/user/activate/account/<string:user_token>',\
                                          view_func=ActivateAccountView.as_view('activate_account', Users, UserToken, template='auth/create_user.html'))
    bp_auth_register_parent.register_blueprint(bp_acc_recover)

