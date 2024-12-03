import json
from bson import ObjectId
from flask import Blueprint, render_template, make_response, request, jsonify
from flask_cors import CORS, cross_origin
from markupsafe import escape

# from ..configs_package import mongodb_connection
from pymongo import MongoClient
from flask import current_app

bp_courses = Blueprint("course", __name__, url_prefix="/course")
CORS(bp_courses)

from ..token_module.userTokenModel import UserToken
from .enroll.enroll_view import EnrollView
from .course.course import CourseModel
from .course.controller import get_courses_by_coursename, save_course_to_mgdb, update_course_to_mgdb
from .content.courses_content import CourseContentModel
from .content.course_content_post_view import CourseContentPostUpdateView
from ..package_learning.elearning.course_progress import CourseProgressModel
from .enroll.enroll import EnrollModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel
from ..package_courses.course.course_post_update_view import CoursePostUpdateView
from ..package_code_editor.code_editor_factory import CodeEditorFactory
from ..utils import __get_cookies, set_header_params

bp_courses.add_url_rule(
    "/post",
    view_func=CoursePostUpdateView.as_view(
        "post", CourseModel, UserToken, __get_cookies, "admin/form_course.html"
    ),
)

bp_courses.add_url_rule(
    "/content/post",
    view_func=CourseContentPostUpdateView.as_view(
        "content_post",
        CourseContentModel,
        UserToken,
        __get_cookies,
        "admin/form_course_content.html",
    ),
)

#
bp_courses.add_url_rule(
    "/enroll/<string:course>",
    view_func=EnrollView.as_view(
        "enroll",
        EnrollModel,
        # "e_learning/enroll_to_course.html"
        CourseModel,
        UserToken,
        CardTransactionModel,
        PaymentModel,
        PaymentCardModel,
        "courses/embedy_payment.html",
    ),
)


# Custom encoder for objectID
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


@bp_courses.route("/create", methods=["GET", "POST"])
@cross_origin(methods=["GET", "POST"])
def create_course():
    
    course_title = escape(request.args.get('course'))
  
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    if request.method == "POST":

        try:
            data = request.get_json()
            objectives = data.get("objectives", [])
            requirements = data.get("requirements", [])
            topics = data.get("topics", [])
            description = data.get("courseDescription")
            course_title = data.get("courseName")
            courseClonedName = data.get("courseClonedName")

            document = {
                "course_code": 4,
                "course_description": description,
                "course_name": course_title,
                "course_objectives": objectives,
                "requirement": requirements,
                "course_curriculum": topics
            }

            # Validate the received data
            if not description or not course_title or not objectives:
                return jsonify({"message": "description, courseName, and objectives are required"}), 400


            # Getting the course data by name from MongoDB
            data = get_courses_by_coursename(connection=connection, course_name=courseClonedName)
            if data:
                status = update_course_to_mgdb(connection=connection, course_name=courseClonedName, document=document)
                respo = f"Your {courseClonedName} data was updated successfully {course_title}"
            else:
                status = save_course_to_mgdb(connection, document)
                respo = f"Your data was saved successfully"
           
            # close the server connecton
            connection.close()
            return jsonify({"response": respo, "doc": ""}), 200
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500
        
    # If the request.method is GET
     
    try:
        
        # Getting the course data by name from MongoDB
        data = get_courses_by_coursename(connection=connection, course_name=course_title)
        response = make_response(
            render_template(
                "courses/add-course.html",
                title="Create Course",
                USER_DATA=__get_cookies,
                course_data=data,
            )
        )
        set_header_params(response)
        return response
    except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500


@bp_courses.route("/list-all")
@cross_origin(methods=["GET"])
def get_all():
    """for item in data:
    status, obj = CourseProgressModel.create(column=courses_rogress)"""

    courses = CourseModel.get()
    courses = [] if len(courses) == 0 else courses

    from ..utils import __get_cookies, set_header_params

    response = make_response(
        render_template(
            "admin/list_courses.html",
            title="All Courses",
            USER_DATA=__get_cookies,
            courses=courses,
        )
    )
    set_header_params(response)
    return response


@bp_courses.route("/courses")
@cross_origin(methods=["GET"])
def courses():
    welcome_title = "Our Courses"
    welcome_message = "Discover a world of knowledge with our diverse range of courses"

    from ..utils import __get_cookies, set_header_params

    response = make_response(
        render_template(
            "courses.html",
            title="Courses",
            welcome_title=welcome_title,
            USER_DATA=__get_cookies,
            welcome_message=welcome_message,
        )
    )

    set_header_params(response)
    return response


@bp_courses.route("/new")
@cross_origin(methods=["GET"])
def new_course():
    welcome_title = "New"
    welcome_message = "Enter a new course"

    from ..utils import __get_cookies, set_header_params

    response = make_response(
        render_template(
            "admin/form_course.html",
            title="New Course",
            USER_DATA=__get_cookies,
            welcome_title=welcome_title,
            welcome_message=welcome_message,
        )
    )

    set_header_params(response)
    return response


@bp_courses.route("/python-courses")
@cross_origin(methods=["GET"])
def python_courses():
    welcome_title = "Python Courses"
    welcome_message = "Master Python programming with our comprehensive courses"

    courses = CourseModel.get()
    courses = [] if len(courses) == 0 else courses

    from ..utils import __get_cookies, set_header_params

    response = make_response(
        render_template(
            "python-courses.html",
            title="Python Courses",
            USER_DATA=__get_cookies,
            courses=courses,
            welcome_title=welcome_title,
            welcome_message=welcome_message,
        )
    )

    set_header_params(response)
    return response


@bp_courses.route("/know-more/<string:course_name>")
@cross_origin(methods=["GET"])
def know_more(course_name):
    link = escape(request.args.get("link"))
    course_name = escape(course_name)

    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])
    # get database list

    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    course = db.courses.find_one({"course_name": course_name})

    # Serialize data
    serialized_data = json.dumps(course, cls=JSONEncoder)
    deserialized_data = json.loads(serialized_data)
    # close the server connecton
    connection.close()

    response = make_response(
        render_template(
            "courses/python_basic_details.html",
            course_payment_link=link,
            title=course_name,
            USER_DATA=__get_cookies,
            welcome_title=course_name,
            course_content=deserialized_data,
        )
    )

    set_header_params(response)
    return response


@bp_courses.route("/view-content/<int:courseID>/<string:description>")
@cross_origin(methods=["GET"])
def list_course_content(courseID, description):
    course_id = escape(courseID)
    _course = escape(description)
    user_token = escape(request.args.get("user_token"))

    status, content = CourseContentModel.get_content_by_course_id(course_id=course_id)
    content = CourseContentModel.convert_to_list(content)

    from ..utils import __get_cookies, set_header_params

    response = make_response(
        render_template(
            "admin/list_courses_content.html",
            title="Courses Content",
            USER_DATA=__get_cookies,
            courses=_course,
            content=content,
        )
    )
    set_header_params(response)
    return response


@bp_courses.route("/content/read-file/<string:topic>")
@cross_origin(methods=["GET"])
def read_file_content(topic):
    fileFormat = escape(request.args.get("format"))
    topic = escape(topic)
    fileName = str(topic).lower().replace(" ", "-")
    directory = "laubcode/root"
    from ..utils.my_file_factory import read_html_file

    # file_path ="html/overview-python.html"
    file_path = f"laubcode/root/{topic}.{fileFormat}"

    filecontent = CodeEditorFactory.read_file(
        directory, f"{directory}/{fileName}.{fileFormat}"
    )

    # content = read_html_file(file_path=file_path)
    # return  jsonify({"topic": topic, "content": filecontent},200)
    return jsonify(
        {"filename": f"{fileName}.{fileFormat}", "content": filecontent}, 200
    )


# Create the mongoDB  instance


@bp_courses.route("/test-mongo")
def test_mongo():
    # connect to mongodb server

    connection = MongoClient(current_app.config["MONGO_URI"])
    # get database list

    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    courses = db.courses.find()
    dd = []

    for cor in courses:
        dd.append(cor)

    course = db.courses.find_one({"course_code": 1})

    # Serialize data
    serialized_data = json.dumps(course, cls=JSONEncoder)
    deserialized_data = json.loads(serialized_data)

    return f"DD: {deserialized_data['course_objectives']}"
