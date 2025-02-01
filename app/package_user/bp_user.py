
from flask import Blueprint, render_template, make_response, request
from flask_cors import  CORS, cross_origin
from markupsafe import escape

bp_user = Blueprint("users", __name__, url_prefix='/users')
CORS(bp_user)

from ..auth_package import Users
from ..token_module.userTokenModel import UserToken
from ..package_courses.enroll.enroll_view import EnrollView

from ..package_learning.elearning.course_progress import CourseProgressModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel
from ..utils import my_cookies
from .module_user.users_view import UsersView

bp_user.add_url_rule("manage",view_func=UsersView.as_view('/manage', Users, UserToken, template="admin/list_users.html"))

@bp_user.route('/')
@cross_origin(methods=['GET'])
def users_all():
    welcome_title = "All Users"
    welcome_message = ""

    status,users = Users.get_all_users()

    response = make_response(render_template('admin/list_users.html', title="Users",USER_DATA = my_cookies.__get_cookies, users=users,  welcome_title=welcome_title, welcome_message=welcome_message))
    response.set_cookie('current_page', 'admin.users.users_all')
    return response

@bp_user.route('/<int:userID>/delete')
@cross_origin(methods=['GET'])
def remove_user(userID):
    userID = escape(userID)
    user_token = escape(request.args.get('user_token', None))

    response = make_response(render_template('admin/list_users.html', title="Users",USER_DATA = my_cookies.__get_cookies, users=users,  welcome_title=welcome_title, welcome_message=welcome_message))
    response.set_cookie('current_page', 'admin.users.users_all')
    return response
    

