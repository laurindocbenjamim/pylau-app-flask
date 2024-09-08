
import re
from flask import Request
from app.utils import is_valid_email, validate_str_and_punct_char, validate_only_str, validate_str_punct_and_digits, validate_str_digits

numbers_pattern = r'^[0-9-]+$'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def validate_words(key:str, value: str | int | float)-> bool:
    """
    This method is  used to validate the form fields
    """

    if key != 'address2' and key != 'bankticket':
        if value is None or value =='':
            return  False, f"{str(key).replace('_', ' ').upper()} is required."
        elif len(str(value).replace(' ', '')) > 100:
            return  False, f"Invalid size for field {str(key).replace('_', ' ').upper()}."
    
    # Checking if the fields have just strings and digits
    if 'csrf_token' == key:
        return True, 'OK'
    
    elif 'email' == key:
        if not is_valid_email(value):
            return False, 'Enter a valid email'
    elif 'address' == key:
        if not validate_str_punct_and_digits(key):
            return False, f"Invalid characters detected on {str(key).replace('_', ' ').upper()} - {value}"
    elif 'zip' == key:
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {str(key).replace('_', ' ').upper()}"
    elif not validate_str_digits(value):
        return False, f"Invalid characters detected on {str(key).replace('_', ' ').upper()} - {value}"
    
    return True, 'OK'


def validate_file(request: Request):
    # check if the post request has the file part
    if 'bankTicket' not in request.files:
        return False, 'No bank ticket part'
        
    file = request.files['bankTicket']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return False, 'No selected file'
        
    if not file:
        return False, "No selected file"
    if not allowed_file(file.filename):
        return False, "Not allowed file"
        
    # Return True if everything is okay
    return True
        
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    