

import re

from flask import flash, Request
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

"""
This controller contain functions to validate the form data

"""

# Filter unauthorized characters
authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_/,.:"
authorized_integer = "0123456789"
authorized_country_code_chars = "0123456789+"
authorized_password_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_!@#$%^&*()_+"
numbers_pattern = r'^[0-9.]+$'

def validate_only_string(s):
        """ This pattern allows spaces, accentuated characters, and common punctuation"""
        
        pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s.,;!?\'"()]+$'
        if re.match(pattern, s):
            return True
        else:
            return False
        
def validate_string_with_digits(s):
    """ This pattern allows spaces, accentuated characters, numbers, and common punctuation """
    #pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;!?#\'"()]+$'
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;!?:-/#"()]+$'
    if re.match(pattern, s):
        return True
    else:
        return False

def validate_words(key:str, value: str | int | float, 
                   required_fields=[], 
                   float_fields=[],
                   float_fields_max_len=10,
                   max_str_len=100,
                   data_types=['str', 'int', 'float']
                   )-> bool:
    """
    First we check what fields are required.
    If the key field received is empty then it returns a message saying t hat the 
    field is required.
    
    """

    # First check if the form field has  not value if true iterate the required fields, 
    # compare  if the key from form is equal to the
    if not value:        
        if key in required_fields:
            return False, f"The {key.replace('_', ' ').upper()} is required"
        
    """
    The code below verify the data types of the field, the size
    and the authorized characteres. If they did not passed to the rules 
    defined the method returns false, otherwise re turns True. 

    """
    #if not isinstance(value, str or int):
    if not isinstance(value, [dtype for dtype in data_types]):
        return False, f"The {key.replace('_', ' ').upper()} must be a string"
        
    if len(value.replace(' ', '')) > max_str_len:
        return False, f"The {key} must have less or equal {max_str_len} characters"
    
    if any(char not in authorized_chars for char in value.replace(' ', '')):
        return False, f"Invalid characters detected on {key.replace('_', ' ').upper()} - {value}"
    
    
    if key in float_fields:
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {key.replace('_', ' ').upper()} - {value}"
        if len(value.replace(' ', '')) > float_fields_max_len:
            return False, f"Invalid size for the {key.replace('_', ' ').upper()} - {value}"
    
    

    return True, "pass"
