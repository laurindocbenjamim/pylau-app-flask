
from flask import Blueprint, render_template, make_response, request
from flask_cors import  CORS, cross_origin

bp_courses = Blueprint("course", __name__, url_prefix='/course')
CORS(bp_courses)

from ..token_module.userTokenModel import UserToken
from .enroll.enroll_view import EnrollView
from .course.course import CourseModel
from .enroll.enroll import EnrollModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel


@bp_courses.route('/list-all')
@cross_origin(methods=['GET'])
def get_all():
    import random
    from datetime import datetime, timezone

    USER_DATA = {
             'USERNAME': request.cookies.get('USERNAME', ''),
        'USER_STATUS': request.cookies.get('USER_STATUS', ''),
        'USER_ROLE': request.cookies.get('USER_ROLE', ''),
        'USER_TOKEN': request.cookies.get('USER_TOKEN', '')
        }
    
    data = [{
        "course_code": f"PYB00{random.choice([1000, 10000])}",
        "course_description": "Python Basic",
        "course_details": "Basic Python course, a bigginer and fundamental course",
        "course_status": 1,
        "course_view_url": "course.learn.python_basic",
        "course_image": "https://page-images.websim.ai/Introduction%20to%20Python_1024x495xMcX91ZnPkVAmUE2bEx39b066e88dcc8.jpg",
        "course_level": "Beginner",
        "course_date_added": datetime.now(),
        "course_year_added": datetime.now().strftime('%Y'),
        "course_month_added": datetime.now().strftime('%m'),
        "course_timestamp_added": datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    },
    {
        "course_code": f"PYB00{random.random()}",
        "course_description": "Python for Data Visualization",
        "course_details": "Python for Data Visualization, an advanced course",
        "course_status": 1,
        "course_image": "https://page-images.websim.ai/Introduction%20to%20Python_1024x495xMcX91ZnPkVAmUE2bEx39b066e88dcc8.jpg",
        "course_view_url": "course.learn.python_for_data_visualize",
        "course_level": "Advanced",
        "course_date_added": datetime.now(),
        "course_year_added": datetime.now().strftime('%Y'),
        "course_month_added": datetime.now().strftime('%m'),
        "course_timestamp_added": datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    }]
    
    for item in data:
        status, obj = CourseModel.create(course=item)

    courses = CourseModel.get()
    courses = [] if len(courses) == 0 else courses
    response = make_response(render_template('admin/list_courses.html', title="All Courses", USER_DATA=USER_DATA, courses=courses))
    return response


#
bp_courses.add_url_rule("/enroll/<string:course>",view_func=EnrollView.as_view("enroll",EnrollModel, 
CourseModel, UserToken, CardTransactionModel,PaymentModel, PaymentCardModel, "e_learning/enroll_to_course.html"))


@bp_courses.route('/courses')
@cross_origin(methods=['GET'])
def courses():
    welcome_title = "Our Courses"
    welcome_message = "Discover a world of knowledge with our diverse range of courses"
    response = make_response(render_template('courses.html', title="Courses",  welcome_title=welcome_title, welcome_message=welcome_message))
    return response
    
@bp_courses.route('/python-courses')
@cross_origin(methods=['GET'])
def python_courses():
    welcome_title = "Python Courses"
    welcome_message = "Master Python programming with our comprehensive courses"

    courses = CourseModel.get()
    courses = [] if len(courses) == 0 else courses

    response = make_response(render_template('python-courses.html', title="Python Courses", courses=courses,  welcome_title=welcome_title, welcome_message=welcome_message))
    return response

