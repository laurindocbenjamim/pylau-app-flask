
import re
import random
from datetime import datetime, timedelta,timezone
from flask import Request
from app.utils import is_valid_email, validate_str_and_punct_char, validate_only_str, validate_str_punct_and_digits, validate_str_digits
from .enroll import EnrollModel
from ...package_payment.payment.payment import PaymentModel
from ...package_payment.payment.payment_card import PaymentCardModel
from ...package_payment.payment.card_transaction import CardTransactionModel

numbers_pattern = r'^[0-9-]+$'
numbers_pattern_card_date = r'^[0-9/]+$'
authorized_country_code_chars = "0123456789-"
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def validate_words(key:str, value: str | int | float)-> bool:
    """
    This method is  used to validate the form fields
    """

    if key != 'address2' and key != 'bankTicket':
        
        if value is None or value =='':
            return  False, f"{str(key).replace(' ', '').upper()} is required."
        elif len(str(value).replace(' ', '')) > 100:
            return  False, f"Invalid size for field {str(key).replace(' ', '_').upper()}."
    
    # Checking if the fields have just strings and digits
    if 'csrf_token' == key:
        return True, 'OK'
    
    elif 'email' == key:
        if not is_valid_email(value):
            return False, 'Enter a valid email'
    elif 'address' == key:
        if not validate_str_punct_and_digits(key):
            return False, f"Invalid characters detected on {str(key).replace(' ', '_').upper()} - {value}"
    elif 'zip' == key:
        if len(str(value).replace(' ','')) > 8:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
    elif 'ccNumber' == key:
        if len(str(value).replace(' ','')) > 20:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
    elif 'ccExpiration' == key:
        if len(str(value).replace(' ','')) > 5:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
        if not re.match(numbers_pattern_card_date, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
    elif 'ccCVV' == key:
        if len(str(value).replace(' ','')) > 3:
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace(' ', '_').upper()}"
    elif value !='':
        if not validate_str_digits(value):
            return False, f"Invalid characters detected on {str(key).replace(' ', '_').upper()} - {value}"
    
    return True, 'OK'


# Save the payment transaction
def create_payment_objects(form: Request.form, **kwargs):
    
    # Creating my objects
    enroll_obj = {}
    card_obj = {}
    payment_obj = {}
    
    if not form.items():
        return False, enroll_obj, card_obj, payment_obj 

    enroll_obj = EnrollModel(
        student_id = kwargs.get('user_id', 0),
        course_id =  form['course_id'],
        student_firstname = form['firstName'],
        student_lastname = form['lastName'],
        student_address = form['address'],
        student_address2 = form['address2'],
        student_country = form['country'],
        student_state = 1,
        same_address = form['sameAddress'],
        student_zip = form['zip'],
        enroll_code = f'{kwargs.get('user_id', 0)}DP-{random.choice([1,6, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 5000, 20000])}',                
        enroll_obs = 'Enrollement course',
        enroll_type = "Test",
        enroll_status = 0,
        enroll_date_added = datetime.now().date(),
        enroll_year_added = datetime.now().strftime('%Y'),
        enroll_month_added = datetime.now().strftime('%m'),
        enroll_timestamp_added = datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    )

    #
    card_obj = PaymentCardModel(
                student_id = kwargs.get('user_id', 0),
                card_number = form['ccNumber'],
                card_name = form['ccName'],
                card_exp = form['ccExpiration'],
                card_cvv = form['ccCVV'],
                card_date_added = datetime.now(),
                card_year_added = datetime.now().strftime('%Y'),
                card_month_added = datetime.now().strftime('%m'),
                card_timestamp_added = datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
            )
    
    payment_obj = PaymentModel(
                student_id = kwargs.get('user_id', 0),
                payment_code = f'{kwargs.get('user_id', 0)}DP-{random.choice([1,6, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 5000, 20000])}',
                payment_method = form['paymentMethod'],              
                payment_date_added = datetime.now(),
                payment_year_added = datetime.now().strftime('%Y'),
                payment_month_added = datetime.now().strftime('%m'),
                payment_timestamp_added = datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
            )
    if form['paymentMethod'] != 'bank reference': 
        payment_obj.card_number = form['ccNumber']
    else:
        payment_obj.payment_reference = kwargs.get('filename', "")
    
    #return True, enroll_obj.serialize(), card_obj.serialize(), payment_obj.serialize()
    return True, enroll_obj, card_obj, payment_obj




    
    