
import re
import random
import json
from bson import ObjectId
from bson.json_util import dumps
from flask import Request
from datetime import datetime, timedelta,timezone
from flask import Request
from app.utils import is_valid_email, validate_str_and_punct_char, validate_only_str, validate_str_punct_and_digits, validate_str_digits
from .course import CourseModel
from ...package_payment.payment.payment import PaymentModel
from ...package_payment.payment.payment_card import PaymentCardModel
from ...package_payment.payment.card_transaction import CardTransactionModel
from app.utils.my_file_factory import validate_file, upload_file

numbers_pattern = r'^[0-9-]+$'
numbers_pattern_card_date = r'^[0-9/]+$'
authorized_country_code_chars = "0123456789-"
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Custom encoder for objectID
class JSONEncoder(json.JSONEncoder):
    """
    This class is used to serilize json data
    """
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)
    
def get_all_courses_mgdb(connection):
    """
    This method has the function to get a course's data from MongoDB

    params:
        connection: receives the mongoDB connection
        course_name: receives the courses's name used  to select the data from the database
    return:
        returns a list of the course's information from the database
    """
    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    courses = db.courses.find()

    # Serialize data
    #serialized_data = json.dumps(course, cls=JSONEncoder)
    #deserialized_data = json.loads(serialized_data)
    result = []
    for doc in courses:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return result

    return deserialized_data

def get_courses_by_coursename(connection, course_name):
    """
    This method has the function to get a course's data from MongoDB

    params:
        connection: receives the mongoDB connection
        course_name: receives the courses's name used  to select the data from the database
    return:
        returns a list of the course's information from the database
    """
    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    course = db.courses.find_one({"course_name": course_name})

    # Serialize data
    serialized_data = json.dumps(course, cls=JSONEncoder)
    deserialized_data = json.loads(serialized_data)

    return deserialized_data

# Method to get the course's content 
def get_courses_content_by_coursename(connection, course_name):
    """
    This method has the function to get a course's content from MongoDB

    params:
        connection: receives the mongoDB connection
        course_name: receives the courses's name used  to select the data from the database
    return:
        returns a list of the course's information from the database
    """
    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    course = db.courses_content.find({"course_name": course_name})

    result = []
    for doc in course:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return result

#
def get_courses_content_by_coursename_and_topic(connection, course_name, course_topic):
    """
    This method has the function to get a course's content from MongoDB

    params:
        connection: receives the mongoDB connection
        course_name: receives the courses's name used  to select the data from the database
    return:
        returns a list of the course's information from the database
    """
    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    course = db.courses_content.find({"course_name": course_name, "course_topic": course_topic})

    result = []
    for doc in course:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return result

# get content's quizz by course, topic a nd module
def get_courses_content_quizzes_by_coursename_topic_module(*,connection, course_name, course_topic,module):
    """ Get get content's quizz by course, topic a nd module 

        Params: 
            connection - the mongodb connection, 
            course_name - the course's name or title, 
            course_topic - the topic of the topic's quizz
            module - the module where the topic belogs to.
        Return: return a list of object with the topic's quizz 
    """

    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    course = db.courses_content.find({"course_name": course_name, "course_topic": course_topic})

    result = []
    for doc in course:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return result

# get content's quizz by course, topic a nd module
def get_courses_content_quizzes_by_coursename_mongo_db(*,connection, course_name):
    """ Get get content's quizz by course name

        Params: 
            connection - the mongodb connection, 
            course_name - the course's name or title
        Return: return a list of object with the course's quizz 
    """

    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    course = db.courses_content_quizzes.find({"course_name": course_name})

    result = []
    for doc in course:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return result

def get_courses_content_quizzes_by_coursename_topic(*,connection, course_name, topic, module):
    """ Get get content's quizz by course name

        Params: 
            connection - the mongodb connection, 
            course_name - the course's name or title
        Return: return a list of object with the course's quizz 
    """

    # Access the database
    db = connection.data_tuning_school

    # Access the collection and retrieve documents
    # docs = db.courses.find()

    course = db.courses_content_quizzes.find({"course_name": course_name, "course_topic": topic, "course_module": module})

    result = []
    for doc in course:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return result


def save_course_to_mgdb(connection, document: dict = {}):
    
    try:
        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses

        # Saving the course information to MongoDB
        collection.insert_one(document)
        return True
    except Exception as e:
        return False


def update_course_to_mgdb(connection, course_name, document: dict = {}):
    
    try:

        query = {"course_name": course_name}

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses

        document = {"$set": document}
        # Saving the course information to MongoDB
        collection.update_one(query, document)
        return True
    except Exception as e:
        return False


def save_courses_content_to_mgdb(connection, document: dict = {}):
    
    try:
        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content

        # Saving the course information to MongoDB
        collection.insert_one(document)
        return True, 'ok'
    except Exception as e:
        return False, str(e)

# Update the course's content document
def update_courses_content_to_mgdb(connection, course_name, course_topic, document: dict = {}):
    
    try:

        query = {"course_name": course_name, "course_topic": course_topic}

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content

        document = {"$set": document}
        # Saving the course information to MongoDB
        collection.update_one(query, document)
        return True
    except Exception as e:
        return False

# Remove the course from MongoDB
def remove_course_from_mgdb(*,connection, query: dict = {}):
    """
    This method removes a course from MongoDB based on the provided query.

    Params:
        connection: The MongoDB connection.
        query: A dictionary containing the query to identify the course to be removed.
    Return:
        A tuple containing a boolean indicating success or failure, and the query or error message.
    """
    try:

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses

        # Removing the course information to MongoDB
        collection.delete_one(query)
        return True, "Ok"
    except Exception as e:
        return False, str(e)
    
# Remove the course's content document
def remove_courses_content_from_mgdb(*,connection, query: dict = {}):
    
    try:

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content

        # Removing the course information to MongoDB
        collection.delete_one(query)
        return True, query
    except Exception as e:
        return False, str(e)

# Save the course's conten quizzes
def save_courses_content_quizzes(connection, document: dict = {}):
    try:
        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content_quizzes

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content_quizzes

        # Saving the course information to MongoDB
        collection.insert_one(document)
        return True, 'ok'
    except Exception as e:
        return False, str(e)

# Remove the course's content quizzes document
def remove_courses_content_quizz_from_mgdb(*,connection, query: dict = {}):
    """
    
    """
    try:

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content_quizzes

        # Access the database
        db = connection.data_tuning_school

        # Access the collection and retrieve documents
        collection = db.courses_content_quizzes

        # Removing the course information to MongoDB
        collection.delete_one(query)
        return True, query
    except Exception as e:
        return False, str(e)


def validate_words(key:str, value: str | int | float)-> bool:
    """
    This method is  used to validate the form fields
    """

    if key != 'courseCertified' and key != 'courseStatus' and key != 'courseTotalModules' and key != 'courseTotalLabs':
        
        if value is None or value =='':
            return  False, f"{str(key).replace('_', '').replace(' ', '').lower()} is required."
        elif len(str(value).replace(' ', '')) > 100:
            return  False, f"Invalid size for field {str(key).replace(' ', '_').lower()}."
    
    # Checking if the fields have just strings and digits
    if 'csrf_token' == key:
        return True, 'OK'
    elif key != 'thumbnail' and value !='':
        if not validate_str_digits(value):
            return False, f"Invalid characters detected on {str(key).replace(' ', '_').lower()} - {value}"
    elif 'courseLevel' == key:
        if len(str(value).replace(' ','')) > 20:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    elif 'courseDescription' == key:
        if len(str(value).replace(' ','')) > 200:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    elif 'courseDetails' == key:
        if len(str(value).replace(' ','')) > 200:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern_card_date, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    elif 'courseViewUrl' == key:
        if len(str(value).replace(' ','')) > 50:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    
    
    return True, 'OK'


# Save the payment transaction
def create_objects(form: Request.form, **kwargs):
    
    if not form.items():
        return {}, [] 
    label =''
    for k,l in enumerate(form["courseDescription"]):
        label+= str(l[0])

    filename = kwargs.get('filename', "")

    selected_options = form.get('courseCertified')

    obj = CourseModel(
        course_code =  f"{str(label).upper()}00{random.choice([1,6, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 5000, 20000])}",
        course_description =  form["courseDescription"],
        course_details =  form["courseDetails"],
        course_status =  1 if form["courseStatus"] =='1' or form["courseStatus"] ==1 else 0,
        course_is_certified = 0 if form.get('courseCertified') is None or form.get('courseCertified')=='None' else 1,
        course_view_url =   str(form["courseViewUrl"]).replace(' ', ''),
        course_image =  kwargs.get('filename', ""),
        course_level =  form["courseLevel"],
        course_total_lessons =  form["courseTotalLessons"],
        course_total_quizzes =  form["courseTotalQuizzes"],
        course_total_labs =  form["courseTotalLabs"] if form["courseTotalLabs"] != '' else 0,
        course_total_modules =  form["courseTotalModules"] if form["courseTotalModules"] !='' else 0,
        course_date_added =  datetime.now(),
        course_year_added =  datetime.now().strftime('%Y'),
        course_month_added =  datetime.now().strftime('%m'),
        course_timestamp_added =  datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    )
    

    listOBJ = {
        "course_code":  f"{str(label).upper()}00{random.choice([1,6, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 5000, 20000])}",
        "course_description":  form["courseDescription"],
        "course_details":  form["courseDetails"],
        "course_status":  1 if form["courseStatus"] =='1' or form["courseStatus"] ==1 else 0,
        "course_is_certified": 0 if form.get('courseCertified') is None or form.get('courseCertified')=='None' else 1,
        "course_view_url":  str(form["courseViewUrl"]).replace(' ', ''),
        "course_image":  kwargs.get('filename', ""),
        "course_level":  form["courseLevel"],
        "course_total_lessons":  form["courseTotalLessons"],
        "course_total_quizzes":  form["courseTotalQuizzes"],
        "course_total_labs":  form["courseTotalLabs"] if form["courseTotalLabs"] != '' else 0,
        "course_total_modules":  form["courseTotalModules"] if form["courseTotalModules"] !='' else 0,
        "course_date_added":  datetime.now(),
        "course_year_added":  datetime.now().strftime('%Y'),
        "course_month_added":  datetime.now().strftime('%m'),
        "course_timestamp_added":  datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    }
    return obj, listOBJ




    
    