

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

def validate_words(key:str, value: str | int | float)-> bool:
    """
    First we check what fields are required.
    If the key field received is empty then it returns a message saying t hat the 
    field is required.
    
    """
    if not value:
        if key in 'product_barcode':
            return False, f"The product barcode is required"
        elif key in 'product_description':
            return False, f"The product description is required"
        elif key in 'sale_price_01':
            return False, f"The sale price 01 is required"
        
    """
    The code below verify the data types of the field, the size
    and the authorized characteres. If they did not passed to the rules 
    defined the method returns false, otherwise re turns True. 

    """
    if not isinstance(value, str or int):
        return False, f"The {key} must be a string"
        
    if len(value.replace(' ', '')) > 100:
        return False, f"The {key} must have less or equal 100 characters"
    
    if any(char not in authorized_chars for char in value.replace(' ', '')):
        return False, f"Invalid characters detected on {key} - {value}"
    
    
    if key in 'sale_price_01':
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {key} - {value}"
        if len(value.replace(' ', '')) > 10:
            return False, f"Invalid size for the {key} - {value}"
    
    

    return True, "pass"
