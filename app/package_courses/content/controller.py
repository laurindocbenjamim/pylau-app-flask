
import re
import random
from datetime import datetime, timedelta,timezone
from flask import Request
from app.utils import is_valid_email, validate_str_and_punct_char, validate_only_str, validate_str_punct_and_digits, validate_str_digits
from .courses_content import CourseContentModel
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
    
    if key != 'thumbnail' and key != 'contentStatus':
        
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
    elif 'countentType' == key:
        if len(str(value).replace(' ','')) > 20:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    elif 'contentModule' == key:
        if len(str(value).replace(' ','')) > 10:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    elif 'contentDescription' == key:
        if len(str(value).replace(' ','')) > 200:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern_card_date, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    elif 'contentFileName' == key:
        if len(str(value).replace(' ','')) > 200:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').lower()}"
    
    
    return True, 'OK'


# Save the payment transaction
def create_objects(form: Request.form, **kwargs):
    
    if not form.items():
        return {}, [] 
    label =''
    for k,l in enumerate(form["contentDescription"]):
        label+= str(l[0])

    filename = kwargs.get('filename', "")

    obj = CourseContentModel(
                course_id = int(form['course_id']),
                content_type = str(form['countentType']).replace(' ', '-').lower(),
                content_module = str(form['contentModule']).replace(' ', ''),
                content_file = str(form['contentFileName']).replace(' ', ''),
                content_description = form['contentDescription'],
                content_thumbnail = kwargs.get('filename', ""),
                content_status = 1 if form["contentStatus"] =='1' or form["contentStatus"] ==1 else 0,           
                content_date_added = datetime.now(),
                content_year_added = datetime.now().strftime('%Y'),
                content_month_added = datetime.now().strftime('%m'),
                content_timestamp_added = datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
            )

    return obj

def create_dict(form: Request.form, **kwargs):
    
    if not form.items():
        return {}, [] 
    label =''
    for k,l in enumerate(form["contentDescription"]):
        label+= str(l[0])

    filename = kwargs.get('filename', "")

    return {
        "course_id": int(form['course_id']),
        "content_type": str(form['countentType']).replace(' ', '-').lower(),
        "content_module": str(form['contentModule']).replace(' ', ''),
        "content_file": str(form['contentFileName']),
        "content_description": form['contentDescription'],
        "content_thumbnail": kwargs.get('filename', ""),
        "content_status": 1 if form["contentStatus"] =='1' or form["contentStatus"] ==1 else 0,           
        "content_date_added": datetime.now(),
        "content_year_added": datetime.now().strftime('%Y'),
        "content_month_added": datetime.now().strftime('%m'),
        "content_timestamp_added": datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    }
    




    
    