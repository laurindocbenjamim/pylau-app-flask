
from flask import Blueprint
from ..views.projectsView import ProjectsView
from ...token_module.userTokenModel import UserToken
from ...auth_package.module_sign_up_sub.views.removeUserAccountView import RemoveUserAccountView
from ...auth_package.module_sign_up_sub.model.users import Users
bp_project_view = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')
bp_project_view.add_url_rule('/list/<string:user_token>', view_func=ProjectsView.as_view('list',Users, UserToken, template='projects.html'))
bp_project_view.add_url_rule('/user/remove/<int:user_id>/<string:user_token>', view_func=RemoveUserAccountView.as_view('user-remove',Users, UserToken))