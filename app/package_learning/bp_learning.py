

from flask import Blueprint, render_template, session, request, make_response
from flask_cors import CORS, cross_origin
from markupsafe import escape

bp_learn = Blueprint("learn", __name__, url_prefix="/learn")
CORS(bp_learn)

from ..token_module.userTokenModel import UserToken
from ..package_courses.enroll.enroll_view import EnrollView
from ..package_courses.course.course import CourseModel
from ..package_courses.enroll.enroll import EnrollModel
from ..package_courses.course.courses_content import CourseContentModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel

from .elearning.my_learning_view import MyLearningView
bp_learn.add_url_rule("my-learning", view_func=MyLearningView.as_view("my_learning",EnrollModel, CourseModel, UserToken, "e_learning/my-learning.html"))


@bp_learn.route('/laubcode-editor')
@cross_origin(methods=['GET'])
def laubcode():
    user_id = session.get('user_id', None)
    course_id = request.args.get('userID')
    course_content = {}

    response = make_response(render_template('e_learning/code_editor/my_code_editor.html', title="LAUBCode"))
    response.set_cookie('current_page', "course.learn.laubcode") 
    return response

@bp_learn.route('/python-basic')
@cross_origin(methods=['GET'])
def python_basic():
    user_id = session.get('user_id', None)
    course_id = request.args.get('userID')
    course_content = {}
    
    if user_id is not None and user_id !='':
        course_content = CourseContentModel.get_content_by_course_id(course_id=course_id)

    response = make_response(render_template('e_learning/courses_content/python_courses/python-basic.html', title="Python Basic", course_content=course_content, current_url="course.learn.python_basic"))
    response.set_cookie('current_page', "course.learn.python_basic") 
    return response

@bp_learn.route('/python-for-data-visualize')
@cross_origin(methods=['GET'])
def python_for_data_visualize():
    current_url="course.learn.python_basic"
    return f"Python for Data visualization"

from ..package_code_editor.bp_editor_view import bp_editor
bp_learn.register_blueprint(bp_editor)

