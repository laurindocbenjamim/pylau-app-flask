import json
import os
from bson import ObjectId
from flask import Blueprint, render_template, make_response, request, jsonify
from flask_cors import CORS, cross_origin
from markupsafe import escape
from datetime import datetime

# from ..configs_package import mongodb_connection
from pymongo import MongoClient


bp_courses = Blueprint("course", __name__, url_prefix="/course")
CORS(bp_courses)
from werkzeug.utils import secure_filename
from flask import current_app
from flask_caching import Cache
from unidecode import unidecode

from ..token_module.userTokenModel import UserToken
from .enroll.enroll_view import EnrollView
from .course.course import CourseModel
from .course.controller import get_courses_by_coursename, save_course_to_mgdb
from .course.controller import save_courses_content_to_mgdb, get_courses_content_by_coursename_and_topic
from .course.controller import get_courses_content_by_coursename
from .course.controller import update_course_to_mgdb
from .course.controller import update_courses_content_to_mgdb, get_all_courses_mgdb
from .course.controller_mongo_db import remove_courses_content_from_mgdb, save_courses_content_quizzes
from .course.controller_mongo_db import get_courses_content_quizzes_by_coursename_mongo_db
from .course.controller_mongo_db import get_courses_content_quizzes_by_coursename_topic
from .course.controller_mongo_db import remove_course_from_mgdb
from .course.controller_mongo_db import remove_courses_content_quizz_from_mgdb

from .content.courses_content import CourseContentModel
from .content.course_content_post_view import CourseContentPostUpdateView
from ..package_learning.elearning.course_progress import CourseProgressModel
from .enroll.enroll import EnrollModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel
from ..package_courses.course.course_post_update_view import CoursePostUpdateView
from ..package_code_editor.code_editor_factory import CodeEditorFactory
from app.utils import __get_cookies, set_header_params
from app.utils.my_file_factory import validate_file
from app.utils.my_file_factory import upload_file
from app.utils.my_file_factory import validate_image_size
from app.utils.my_file_factory import delete_directory_with_contents

#
main_folder = 'tutorials' #

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

ALLOWED_EXTENSIONS = {'mp4', 'webm', 'mkv', 'avi'}

def allowed_file(filename):
    """Check if a file is an allowed type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#
def save_file_with_new_name(file, original_name, file_path): 
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S') 
    new_name = f"{str(os.path.splitext(original_name)[0]).replace(' ','_')}_{timestamp}{os.path.splitext(original_name)[1]}" 
    file.save(os.path.join(file_path, secure_filename(new_name))) 
    return new_name

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
    filename = ''
    status = True
    message = ""
    file_field_name='thumbnail'

    def upload_thumbnail(folder,file_field_name='thumbnail'):
       
        try:
            if f'{file_field_name}' in request.files:
                
                file = request.files[f'{file_field_name}']
               
                if file.filename != '':
                # Validate the thumbnail file                  
                    status, message = validate_file(request=request, file_field_name=file_field_name)
                   
                    if not status:
                        return status, message
                    else:
                        status, filename = upload_file(request_file=request.files, file_field_name=file_field_name, folder=folder, save_with='new')
                        
                        # validate the size of the image
                        if status and validate_image_size(f'{folder}{filename}'): 
                            return True, filename
                        else: os.remove(filename) 
                        return False, 'Invalid image size or dimensions'
                return status, filename
        except Exception as e:
            return False, str(e)
        
    
    course_title = escape(request.args.get('course', ''))
    thumbnail = ""

    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    if request.method == "POST":

        try:
            # Changing the way to get data from client form request because with request.get_json() 
            # is not possible to get uploaded file data
            """data = request.get_json()
            objectives = data.get("objectives", [])
            requirements = data.get("requirements", [])
            topics = data.get("topics", [])
            description = data.get("courseDescription")
            course_title = data.get("courseName")
            courseClonedName = data.get("courseClonedName")"""

            objectives = json.loads(request.form.get('objectives'))
            requirements = json.loads(request.form.get('requirements'))
            topics = json.loads(request.form.get('topics'))
            description = request.form.get("courseDescription")
            course_title = request.form.get("courseName")
            courseClonedName = request.form.get("courseClonedName")
            old_thumbnail_file = request.form.get("thumbnail_file", '')
            
            #
            folder = f'{main_folder}/{str(unidecode(course_title).replace(' ','_').lower())}/'
            status, filename = upload_thumbnail(folder=folder)
            
            
            if status:                
                filename = f'{folder}{filename}'
            else: message = filename

            
            document = {
                "course_code": 4,
                "course_description": description,
                "course_name": str(course_title.rstrip()).lstrip(),
                "course_objectives": objectives,
                "requirement": requirements,
                "course_curriculum": topics,
                "thumbnail": filename
            }

            # Validate the received data
            if not description or not course_title or not objectives:
                return jsonify({"status_code": 400, "response": "description, courseName, and objectives are required"}), 400


            # Getting the course data by name from MongoDB
            data = get_courses_by_coursename(connection=connection, course_name=courseClonedName)
            
            if data:
                file = request.files[f'{file_field_name}']
                if old_thumbnail_file and file.filename == '':
                    document['thumbnail'] = old_thumbnail_file

                status = update_course_to_mgdb(connection=connection, course_name=courseClonedName, document=document)
                respo = f"Your {courseClonedName} data was updated successfully {course_title}"
            else:
                status = save_course_to_mgdb(connection, document)
                respo = f"Your data was saved successfully"
           
            # close the server connecton
            connection.close()
            message = f'{message}. {respo}'
            return jsonify({"status_code": 200, "response": message, "doc": filename}), 200
        except Exception as e:
            return jsonify({"status_code": 500, "response": f"An error occurred. {str(e)}", "error": str(e)}), 201
        
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


#
@bp_courses.route("/delete-course/<string:course>", methods=["DELETE"])
@cross_origin(methods=["DELETE"])
def delete_course(course):

    course_title = escape(course)
   
    message = f"Failed to delete the {course_title} course."
    
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

     # Getting the course data by name from MongoDB
    try:
        data = get_courses_by_coursename(connection=connection, course_name=course_title)
        if not data:
            message = f"The course <<{course_title}>> does not exist."
        else:
            # Check if the course has content if so, remove it
            data = get_courses_content_by_coursename(connection=connection, course_name=course_title)
            if data:
                sts, resp = remove_courses_content_from_mgdb(connection=connection, query = {"course_name": course_title})
                if not sts:
                    return jsonify({"status_code":201, "response": f"Failed to remove the course's content. {resp}"}), 200

            # Check if the course has quizz content if so, remove it
            course_content_quizzes = get_courses_content_quizzes_by_coursename_mongo_db(connection=connection,course_name=course_title)
            if course_content_quizzes:
                sts, resp = remove_courses_content_quizz_from_mgdb(connection=connection, query = {"course_name": course_title})
                if not sts:
                    return jsonify({"status_code":201, "response": f"Failed to remove the course's quizz content. {resp}"}), 200

            # Delete the course's thumbnail
            directory = f'{current_app.config['UPLOAD_FOLDER']}/{main_folder}/{str(unidecode(course_title).replace(' ','_').lower())}'
            status, message = delete_directory_with_contents(directory=directory)
            # Remove the course from the database
            if status:
                status, message = remove_course_from_mgdb(connection=connection, query={"course_name": str(course_title)})
                if status:
                    return jsonify({"status_code":200, "response": f"The course <<{str(course_title)}>> has been successfully deleted. {message}"}), 200                        
            else:
                message = f"Failed to delete the course. {message}"
        return jsonify({"status_code":400, "response": f"{message}. ({course_title})"}), 200  
    except Exception as e:
        return jsonify({"status_code":500, "response": f"{str(e)}. ({course_title})"}), 200


@bp_courses.route("/create-content", methods=["GET", "POST"])
@cross_origin(methods=["GET", "POST"])
def create_course_content():
    
    course_title = escape(request.args.get('course'))
    courses_module = set()
    
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    if request.method == "POST":
        
            

        file_field_name = "videoFile"
        video = ""
            
        if 'courseTopic' not in request.form or not request.form['courseTopic']:
            return jsonify({"error": "The course's topic is required"}), 201        
        elif 'courseContentOrigin' not in request.form or not request.form['courseContentOrigin']:
            return jsonify({"error": "The origin of the content is required"}), 201
        elif 'courseTitle' not in request.form or not request.form['courseTitle']:
            return jsonify({"error": "The course's title is required"}), 201

        #
        # 
        course_module = request.form.get('courseModule', '')
        course_title = request.form['courseTitle']
        topic = request.form['courseTopic']
        file_origin = request.form['courseContentOrigin']
        
         
        if request.form['courseContentOrigin'] == 'youtube' or request.form['courseContentOrigin'] == 'remote-server':
            if  f'{file_field_name}' not in request.form or not request.form[f'{file_field_name}']:
                return jsonify({"error": "The file video is required"}), 201
            else: 
                save_path = request.form[f'{file_field_name}']

        elif request.form['courseContentOrigin'] == 'localhost':
            if  f'{file_field_name}' not in request.files:
                return jsonify({"error": "The file video required"}), 201
            else:     
                                        
                video = request.files['videoFile']
                    #
                folder=f'{main_folder}/{str(unidecode(course_title).replace(' ','_').lower())}/'

                if 'oldVideoFile' in request.form and request.form['oldVideoFile'] and not video.filename:
                    save_path = request.form['oldVideoFile']
                else:

                    if not video.filename:
                        return jsonify({"status_code":400, "error": "The video file is required!"}), 201
                        
                    # Validate file
                    if not allowed_file(video.filename):
                        return jsonify({"status_code":400, "error": "Invalid video file type"}), 201
                        
                    UPLOAD_FOLDER = f'{current_app.config['UPLOAD_FOLDER']}/{folder}'
                    
                    # Check if the folder to store the tickets exists, if not, create it
                    try:
                        if not os.path.exists(UPLOAD_FOLDER):
                            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    except Exception as e:
                        return jsonify({"status_code":400, "response": f"Failed to create the file path. {e}"}), 200 

                    try:
                        # Add write permission to the directory
                        os.chmod(UPLOAD_FOLDER, 0o777) # Grants all permissions
                        #os.chmod(UPLOAD_FOLDER, 0o755) # Grants Read and Execute only
                
                        # Join the file with its path
                        #save_path = os.path.join(UPLOAD_FOLDER, secure_filename(video.filename.replace('\\', '/')))
                        #video.save(save_path)   
                        save_path = save_file_with_new_name(video, video.filename, UPLOAD_FOLDER)
                        save_path = f'{UPLOAD_FOLDER}{save_path}'
                        # Using close() method 
                        # file = open('path/to/file.txt', 'r') 
                        # Perform file operations 
                        # file.close()
                    
                        if not os.path.exists(save_path): 
                            # Revoke write privileges
                            #os.chmod(UPLOAD_FOLDER, 0o555)   
                            return jsonify({"status_code":400, "response": f"File was not uploaded. {save_path} "}), 200 
                        else:
                            os.chmod(save_path, 0o644) # Grant Read and Execute file
                    except Exception as e:                        
                        # Revoke write privileges
                        #os.chmod(UPLOAD_FOLDER, 0o555)
                        return jsonify({"status_code":400, "response": f"File was not uploaded. {e}"}), 200 
                            

                    # Revoke write privileges
                    os.chmod(UPLOAD_FOLDER, 0o555)         
            
        
            
        document = {                
            "course_name": course_title,
            "file_origin": file_origin,
            "course_topic": topic,
            "course_content_file": str(save_path).replace('app/static/', '')
        }

        if course_module and course_module !='':
            document["course_module"] = course_module
           
        try:
            # Getting the course data by name from MongoDB
            course_content = get_courses_content_by_coursename_and_topic(connection=connection, course_name=course_title, course_topic=topic)
            #return jsonify({"course": course_title, "topic": topic, "response": course_content}), 201
            if course_content and len(course_content) > 0:
                status = update_courses_content_to_mgdb(connection=connection, course_name=course_title, course_topic=topic, document=document)
                #respo = f"Your {content} data was updated successfully {course_title}"
                
                return jsonify({"status_code": 200, "response": "Document updated successfully!"}), 200
            else:
                
                status, sms = save_courses_content_to_mgdb(connection, document)
                
                if not status:
                    document = f"Failed to save the course's content! {sms}"
                else: 
                    document = f"Document saved successfully! {sms}"
            # close the server connecton
            connection.close()
            return jsonify({"status_code": 200, "response": document, "sms": sms}), 200
        except Exception as e:
            connection.close()
            return jsonify({"status_code": 400, "message": "An error occurred", "error": str(e)}), 200
        
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


# Create the courses quizes with Open AI
@bp_courses.route("/create-content/quizzes/<string:course>/<string:topic>", methods=["GET", "POST"])
@cross_origin(methods=["GET", "POST"])
def create_courses_quizes(course,topic):
    course_title = escape(course)
    topic = escape(topic)
    module = escape(request.args.get('module'))
    courses_module = set()
    
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    if request.method == 'POST':
        prompt = """
                    You are a software engineer. 
                    Your task is to return only an object with two columns: script, recomendations.
                    Remember to return the requested script.
                    Add comments to the generated script.
                    Follow the best practices of the UX (User Experience) and UI (User Interface) development patterns.
                """
        prompt = f"""
                    {prompt} 
                        \n{request.form.get('prompt')}
                    """

        message =""
        from app.package_prompts.code_generator.dev_AI_assistant import validate_string_with_digits,get_completion, gpt_model

        
        try:
            if prompt is None:
                return jsonify({"status_code":201, "data": "No prompt has been received."})
            #elif not validate_string_with_digits(prompt):   
            #    return jsonify({"status_code":201, "data": "Invalid characters where found in your prompt"})
            else:
                
                prompt = f"""
                {prompt} 
                            {request.form.get('prompt')}
                            
                            Do not return the steps to create it instead, you create the requested task.
                        """
                completion = get_completion(prompt, gpt_model[1])

                return jsonify({"status_code":200, "prompt": prompt, "data": completion})
        except Exception as e:
            return jsonify({"status_code":400, "data": f"Failed to prompt {str(e)}"})

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
                "courses/add-course-content-quizzes.html",
                title="Create C.C.Quizzes",
                USER_DATA=__get_cookies,
                courses_topic = topic,
                courses_module = module,
                course_name=course_title
            )
        )
        set_header_params(response)
        return response
    except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500


# Save script in mongodb
@bp_courses.route("/save-script-quizzes/<string:course>/<string:topic>", methods=["GET", "POST"])
@cross_origin(methods=["GET", "POST"])
def save_courses_quizzes_to_mongodb(course,topic):
    course_title = escape(course)
    topic = escape(topic)
    module = escape(request.args.get('module'))

    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    try:
        script = request.form.get('script', '')
        course_title = request.form['course']
        module = request.form['module']
        topic = request.form['topic']
            
        document = {    
            "script": script,            
            "course_name": course_title,
            "course_topic": f'{topic}-{datetime.now().strftime('%Y%m%d_%H%M%S')}',
            "course_module": module,
            "datetime": datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        }           
            
        # Getting the course data by name from MongoDB
        #course_content = get_courses_content_by_coursename_and_topic(connection=connection, course_name=course_title, course_topic=topic)
        #return jsonify({"course": course_title, "topic": topic, "response": course_content}), 201
        #if course_content and len(course_content) > 0:
        #    status = update_courses_content_to_mgdb(connection=connection, course_name=course_title, course_topic=topic, document=document)
            #respo = f"Your {content} data was updated successfully {course_title}"
                
        #    return jsonify({"status_code": 200, "response": "Document updated successfully!"}), 200
        #else:
        #return jsonify({"data": document, "status_code": 200, "message": "script saved successfully!"})        
        status, sms = save_courses_content_quizzes(connection, document)
                
        if not status:
            document = f"Failed to save the course's quizz! {sms}"
        else: 
            document = f"Document saved successfully! {sms}"
            # close the server connecton
        connection.close()
        return jsonify({"status_code": 200, "message": document, "error": sms}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "status_code": 500, "error": str(e)}), 200
    



# remove course content from mongoDB
@bp_courses.route("/remove-content", methods=["DELETE"])
@cross_origin(methods=["DELETE"])
def remove_course_content():

    #
    def remove_file(UPLOAD_FOLDER, file_path):
        
        try:
            # os.chmod(UPLOAD_FOLDER, 0o777) # Grant all permitions
            os.chmod(UPLOAD_FOLDER, 0o755) # Grants permition to Read and Execute only
            
            if os.path.exists(file_path): 
                os.chmod(file_path, 0o644)
                os.remove(file_path)
                return True, 'OK'
            return False, 'File not found!'
        except FileNotFoundError as e:
            return False,str(e)
        except Exception as e:
            return False,str(e)

    course_title = escape(request.args.get('course'))
    
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])
    course_title = request.form.get('courseTitle', '')
    course_topic = request.form.get('courseTopic', '')
    course_file_origin = request.form.get('courseFileOrigin', '')
    course_file_path = request.form.get('courseFilePath', '')
    course_module = request.form.get('courseModule', '')
    
    file_removed = True
    f_sms = ''
    
    query = {"course_name": course_title,
            "course_topic": course_topic
            }
    if course_module and course_module !='':
        query["course_module"] = course_module

    if course_file_origin == 'localhost':
        obj_file = str(course_file_path).split('/')

        UPLOAD_FOLDER = f'{current_app.config['UPLOAD_FOLDER']}/{main_folder}/'
        file_path = os.path.join(UPLOAD_FOLDER, obj_file[-1])
        
        file_removed, f_sms = remove_file(UPLOAD_FOLDER, file_path)
    #return jsonify({"status_code":201,"response": f"Failed to remove the course's content {file_path}", "data": f_sms}), 201    
    #            
    try:
        sts, resp = remove_courses_content_quizz_from_mgdb(connection=connection, query=query)
        if not sts:
            return jsonify({"status_code":201,"response": f"Failed to remove the quizzes content."}), 201
        
        sts, resp = remove_courses_content_from_mgdb(connection=connection, query=query)

        resp =f'{resp} && file removed? {file_removed} - {f_sms}'
        if not sts:
            return jsonify({"status_code":201,"response": f"Failed to remove the course's content{resp}"}), 201
        return  jsonify({"status_code":200,"response": f"Content removed successfully!", "data": resp}), 200
    except Exception as e:    
        return  jsonify({"response": f"Failed to remove content {str(e)}"}), 201

# View the courses demo
@bp_courses.route("/view-demo", methods=["GET"])
@cross_origin(methods=["GET"])
def view_courses_demo():

    course_title = escape(request.args.get('course'))
    courses_module = set()
    

     # If the request.method is GET
    # connect to mongodb server
    connection = MongoClient(current_app.config["MONGO_URI"])

    try:
        
        # Getting the course data by name from MongoDB
        data = get_courses_by_coursename(connection=connection, course_name=course_title)
        course_content = get_courses_content_by_coursename(connection=connection, course_name=course_title)
        course_content_quizzes = get_courses_content_quizzes_by_coursename_mongo_db(connection=connection,course_name=course_title)
        
        
        if course_content:
            for course in course_content:
                if 'course_module' in course:
                    courses_module.add(course['course_module'])
        courses_module = list(courses_module) 

        # Store the quizz's content to the Cache Memory
        # Remove spaces and accentuations from string
        cache_course_key_object = f'{str(unidecode(course_title)).replace(' ','_')}_content_quizz'
        cacheQuizz = Cache(current_app)
        # check if the key value already exists if not create it
        cache_object = cacheQuizz.get(str(cache_course_key_object).lower())
        if cache_object is None:
            cacheQuizz.set(str(cache_course_key_object).lower(), course_content_quizzes)

        cache_object = cacheQuizz.get(str(cache_course_key_object).lower())
    
        response = make_response(
            render_template(
                "courses/course_demo.html",
                title="Course Demo",
                USER_DATA=__get_cookies,
                course_data=data,
                course_content=course_content,
                modules = courses_module,
                course_name=course_title,
                course_content_quizzes=course_content_quizzes
            )
        )
        set_header_params(response)
        return response
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


# Get the quizze's content
@bp_courses.route("/get-courses-quizz-content/<string:course>/<string:topic>", methods=["GET", "POST"])
@cross_origin(methods=["GET", "POST"])
def get_courses_quizz_content(course, topic):
    course = escape(course)
    topic = escape(topic)
    module = escape(request.args.get('module'))

    connection = MongoClient(current_app.config["MONGO_URI"])
    if request.method == 'POST':
       """
       
        data = request.get_json()
        exercices_done = data.get("exerc_done", [])
        COURSE = data.get('course')
        return jsonify({"status_code": 200, "EXERCICES_DONE": exercices_done, "COURSE": COURSE}), 200
       """
       return jsonify({"status_code":200}), 200
    
    else:
        if not course and not topic:
            return jsonify({"status_code": 400, "message": "Provide a course's name and topic."}),200

        # Store the quizz's content to the Cache Memory
        # Remove spaces and accentuations from string
        cache_course_key_object = f'{str(unidecode(course)).replace(' ','_')}_content_quizz'
        cacheQuizz = Cache(current_app)
        # check if the key value already exists if not create it
        cache_object = cacheQuizz.get(str(cache_course_key_object).lower())
        course_content_quizzes = []

        if cache_object is None:
            course_content_quizzes = get_courses_content_quizzes_by_coursename_topic(connection=connection,course_name=course, topic=topic, module=module)
            cacheQuizz.set(str(cache_course_key_object).lower(), course_content_quizzes)

        cache_object = cacheQuizz.get(str(cache_course_key_object).lower())
        #
        quizz_content = []

        for item in course_content_quizzes:
            if item['course_topic'] == topic:
                quizz_content.append(item['script'])
            else:
                break
            
        
        return jsonify({"status_code": 200, "script": quizz_content }),200

@bp_courses.route("/get-courses-quizz-content/view-quizz/<string:course>/<string:topic>", methods=["GET"])
@cross_origin(methods=["GET"])
def view_quizz(course,topic):

    course_title = escape(course)
    topic = escape(topic)
    courses_module = escape(request.args.get('courses_module'))

    response = make_response(
        render_template(
            "courses/view_quizz.html",
            title=unidecode(course_title),
            USER_DATA=__get_cookies,
            course_module = courses_module,
            course_name=course_title,
            course_topic=topic,
        )
    )
    set_header_params(response)
    return response

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
