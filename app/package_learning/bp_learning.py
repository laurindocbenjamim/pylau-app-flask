

from flask import Blueprint, render_template
from flask_cors import CORS, cross_origin

bp_learn = Blueprint("learn", __name__, url_prefix="/learn")
CORS(bp_learn)

from ..token_module.userTokenModel import UserToken
from ..package_courses.enroll.enroll_view import EnrollView
from ..package_courses.course.course import CourseModel
from ..package_courses.enroll.enroll import EnrollModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel

from .elearning.my_learning_view import MyLearningView
bp_learn.add_url_rule("my-learning", view_func=MyLearningView.as_view("my_learning",EnrollModel, CourseModel, UserToken, "e_learning/my-learning.html"))

@bp_learn.route('/python-basic')
@cross_origin(methods=['GET'])
def python_basic():

    return render_template('e_learning/python_courses/python-basic.html', title="Python Basic", current_url="course.learn.python_basic")

@bp_learn.route('/python-for-data-visualize')
@cross_origin(methods=['GET'])
def python_for_data_visualize():
    current_url="course.learn.python_basic"
    return f"Python for Data visualization"