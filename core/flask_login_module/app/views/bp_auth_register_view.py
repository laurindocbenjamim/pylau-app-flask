
import flask
from ..model.users import Users
from .authRegisterView.auth_register_view import AuthRegisterView


bp_auth_parent = flask.Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')
bp_auth_parent.add_url_rule('/user/register', view_func=AuthRegisterView.as_view('register', Users, template='create_user.html'))
