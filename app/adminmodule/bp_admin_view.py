
from flask import Blueprint
from .adminView import AdminView
from ..user_module.model.users import Users
from ..token_module.userTokenModel import UserToken

bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')
bp.add_url_rule('/dashboard/<string:user_token>', view_func=AdminView.as_view('dashboard', Users, UserToken, template='admin/dashboard.html'))