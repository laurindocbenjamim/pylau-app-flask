
import re
import random
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




    
    