import json
import os
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
from .course.controller import get_courses_by_coursename, save_course_to_mgdb, save_courses_content_to_mgdb, get_courses_content_by_coursename_and_topic
from .course.controller import get_courses_content_by_coursename, update_course_to_mgdb, update_courses_content_to_mgdb, get_all_courses_mgdb

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

@bp_courses.route("/list-all", methods=["GET"])
@cross_origin(methods=["GET"])
def list_all_courses():
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    try:
        
        # Getting the course data by name from MongoDB
        data = get_all_courses_mgdb(connection=connection)
        
        response = make_response(
            render_template(
                "courses/courses-list.html",
                title="All Course",
                USER_DATA=__get_cookies,
                courses=data
            )
        )
        set_header_params(response)
        return response
    except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

@bp_courses.route("/create", methods=["GET", "POST"])
@cross_origin(methods=["GET", "POST"])
def create_course():
    
    course_title = escape(request.args.get('course', ''))
  
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
                course_name=course_title
            )
        )
        set_header_params(response)
        return response
    except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500


from app.utils.my_file_factory import validate_file, upload_file
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'mp4', 'webm', 'mkv', 'avi'}

def allowed_file(filename):
    """Check if a file is an allowed type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp_courses.route("/create-content", methods=["GET", "POST"])
@cross_origin(methods=["GET", "POST"])
def create_course_content():
    
    course_title = escape(request.args.get('course'))
    courses_module = set()
  
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    if request.method == "POST":

        try:    

            file_field_name = "videoFile"
            if  f'{file_field_name}' not in request.files:
                return jsonify({"error": "Title and age are required"}), 400
            elif 'courseTopic' not in request.form:
                return jsonify({"error": "The course's topic is required"}), 400        
            elif 'courseContentOrigin' not in request.form:
                return jsonify({"error": "The origin of the content is required"}), 400
            elif 'courseTitle' not in request.form:
                return jsonify({"error": "The course's title is required"}), 400
                        
            
            video = request.files['videoFile']
            #
            folder='tutorials'
           
            if not video.filename:
                return f"Ola {video.filename}"
            
             # Validate file
            if not allowed_file(video.filename):
                return jsonify({"error": "Invalid video file type"}), 400
            
            UPLOAD_FOLDER = f'{current_app.config['UPLOAD_FOLDER']}/{folder}'
            
            # Check if the folder to store the tickets exists, if not, create it
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Join the file with its path
            save_path = os.path.join(UPLOAD_FOLDER, secure_filename(video.filename))
            video.save(save_path)
            
            course_module = request.form.get('courseModule', '')
            course_title = request.form['courseTitle']
            topic = request.form['courseTopic']
            file_origin = request.form['courseContentOrigin']
            
            document = {                
                "course_name": course_title,
                "file_origin": file_origin,
                "course_topic": topic,
                "course_content_file": save_path
            }

            if course_module and course_module !='':
                document["course_module"] = course_module
           
            
            # Getting the course data by name from MongoDB
            course_content = get_courses_content_by_coursename_and_topic(connection=connection, course_name=course_title, course_topic=topic)
            #return jsonify({"course": course_title, "topic": topic, "response": course_content}), 201
            if course_content and len(course_content) > 0:
                status = update_courses_content_to_mgdb(connection=connection, course_name=course_title, course_topic=topic, document=document)
                #respo = f"Your {content} data was updated successfully {course_title}"
                
                return jsonify({"response": "Document updated successfully!"}), 201
            else:
                
                status, sms = save_courses_content_to_mgdb(connection, document)
                
                if not status:
                    document = f"Failed to save the course's content! {sms}"
                else: 
                    document = f"Document saved successfully! {sms}"
            # close the server connecton
            connection.close()
            return jsonify({"response": document, "sms": sms}), 201
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500
        
    # If the request.method is GET
     
    try:
        
        # Getting the course data by name from MongoDB
        data = get_courses_by_coursename(connection=connection, course_name=course_title)
        course_content = get_courses_content_by_coursename(connection=connection, course_name=course_title)

        if course_content:
            for course in course_content:
                if 'course_module' in course:
                    courses_module.add(course['course_module'])
        courses_module = list(courses_module) 

     
        response = make_response(
            render_template(
                "courses/add-course-content.html",
                title="Create Course Content",
                USER_DATA=__get_cookies,
                course_data=data,
                course_content=course_content,
                modules = courses_module,
                course_name=course_title
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
