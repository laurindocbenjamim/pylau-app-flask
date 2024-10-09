
from flask import Blueprint, render_template, make_response, request
from flask_cors import  CORS, cross_origin

bp_courses = Blueprint("course", __name__, url_prefix='/course')
CORS(bp_courses)

from ..token_module.userTokenModel import UserToken
from .enroll.enroll_view import EnrollView
from .course.course import CourseModel
from .content.courses_content import CourseContentModel
from .content.course_content_post_view import CourseContentPostUpdateView
from ..package_learning.elearning.course_progress import CourseProgressModel
from .enroll.enroll import EnrollModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel
from ..package_courses.course.course_post_update_view import CoursePostUpdateView
from ..utils import __get_cookies

bp_courses.add_url_rule("/post",view_func=CoursePostUpdateView.as_view("post",CourseModel, UserToken, __get_cookies, "admin/form_course.html"))

bp_courses.add_url_rule("/content/post",view_func=CourseContentPostUpdateView.as_view("content_post",CourseContentModel, UserToken, __get_cookies, "admin/form_course_content.html"))

#
bp_courses.add_url_rule("/enroll/<string:course>",view_func=EnrollView.as_view("enroll",EnrollModel, 
CourseModel, UserToken, CardTransactionModel,PaymentModel, PaymentCardModel, "e_learning/enroll_to_course.html"))


@bp_courses.route('/list-all')
@cross_origin(methods=['GET'])
def get_all():
    import random
    from datetime import datetime, timezone
    
    courses_rogress = [{
        "course_id": 1,
        "student_id": 1,
        "total_lesson_completed": 0,
        "last_lesson_completed": "",
        "date_added": datetime.now(),
        "year_added": datetime.now().strftime('%Y'),
        "month_added": datetime.now().strftime('%m'),
        "timestamp_added": datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    },
    {
        "course_id": 2,
        "student_id": 1,
        "total_lesson_completed": 0,
        "last_lesson_completed": "",
        "date_added": datetime.now(),
        "year_added": datetime.now().strftime('%Y'),
        "month_added": datetime.now().strftime('%m'),
        "timestamp_added": datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    }
    ]
    
    """for item in data:
        status, obj = CourseProgressModel.create(column=courses_rogress)"""

    courses = CourseModel.get()
    courses = [] if len(courses) == 0 else courses

    from ..utils import __get_cookies, set_header_params

    response = make_response(render_template('admin/list_courses.html', title="All Courses", USER_DATA=__get_cookies, courses=courses))    
    set_header_params(response)
    return response




@bp_courses.route('/courses')
@cross_origin(methods=['GET'])
def courses():
    welcome_title = "Our Courses"
    welcome_message = "Discover a world of knowledge with our diverse range of courses"

    from ..utils import __get_cookies, set_header_params

    response = make_response(render_template('courses.html', title="Courses",  welcome_title=welcome_title, USER_DATA=__get_cookies, welcome_message=welcome_message))
    
    set_header_params(response)
    return response

@bp_courses.route('/new')
@cross_origin(methods=['GET'])
def new_course():
    welcome_title = "New"
    welcome_message = "Enter a new course"
    
    from ..utils import __get_cookies, set_header_params
    response = make_response(render_template('admin/form_course.html', title="New Course",USER_DATA=__get_cookies,  welcome_title=welcome_title, welcome_message=welcome_message))
    
    set_header_params(response)
    return response


@bp_courses.route('/python-courses')
@cross_origin(methods=['GET'])
def python_courses():
    welcome_title = "Python Courses"
    welcome_message = "Master Python programming with our comprehensive courses"

    courses = CourseModel.get()
    courses = [] if len(courses) == 0 else courses

    from ..utils import __get_cookies, set_header_params

    response = make_response(render_template('python-courses.html', title="Python Courses",USER_DATA=__get_cookies, courses=courses,  welcome_title=welcome_title, welcome_message=welcome_message))
    
    set_header_params(response) 
    return response

