

import re

from flask import flash, Request
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

# Filter unauthorized characters
authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_/,.:"
authorized_integer = "0123456789"
authorized_country_code_chars = "0123456789+"
authorized_password_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_!@#$%^&*()_+"
numbers_pattern = r'^[0-9.]+$'

def validate_only_string(s):
        # This pattern allows spaces, accentuated characters, and common punctuation
        pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s.,;!?\'"()]+$'
        if re.match(pattern, s):
            return True
        else:
            return False
        
def validate_string_with_digits(s):
    # This pattern allows spaces, accentuated characters, numbers, and common punctuation
    #pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;!?#\'"()]+$'
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;!?:-/#"()]+$'
    if re.match(pattern, s):
        return True
    else:
        return False

def validate_words(key:str, value: str | int | float)-> bool:
    if not value:
        if key in 'product_barcode':
            return False, f"The {key} is required"
        elif key in 'product_description':
            return False, f"The {key} is required"
        elif key in 'product_unitary_price':
            return False, f"The {key} is required"
        elif key in 'product_iva':
            return False, f"The {key} is required"
        elif key in 'product_iva_code':
            return False, f"The {key} is required"
        elif key in 'product_profit':
            return False, f"The {key} is required"
        elif key in 'product_quantity':
            return False, f"The {key} is required"
                
    if not isinstance(value, str or int):
        return False, f"The {key} must be a string"
        
    if len(value.replace(' ', '')) > 100:
        return False, f"The {key} must have less or equal 100 characters"
    
    if any(char not in authorized_chars for char in value.replace(' ', '')):
        return False, f"Invalid characters detected on {key} - {value}"
    #if not validate_string_with_digits(value):
        #return False, f"Invalid characters detected on {key} - {value}"
    
    if key in 'product_quantity':
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {key}"
        if len(value.replace(' ', '')) > 10:
            return False, f"Invalid size for the {key} - {value}"
        
    
    elif key in 'product_profit':
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {key}"
        if len(value.replace(' ', '')) > 5:
            return False, f"Invalid size for the {key} - {value}"
        
    elif key in 'product_iva_code':
        if not isinstance(value, str or int):
            return False, f"Invalid type value for the {key}"
        if len(value.replace(' ', '')) > 10:
            return False, f"Invalid size for the {key} - {value}"
    
    elif key in 'stock_code':
        if not isinstance(value, str or int):
            return False, f"Invalid type value for the {key}"
        if len(value.replace(' ', '')) > 10:
            return False, f"Invalid size for the {key} - {value}"
        
    elif key in 'product_unitary_price':
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {key} - {value}"
        if len(value.replace(' ', '')) > 10:
            return False, f"Invalid size for the {key} - {value}"
    elif key in 'product_iva':
        if not re.match(numbers_pattern, value):
            return False, f"Invalid type value for the {key} - {value}"
        if len(value.replace(' ', '')) > 10:
            return False, f"Invalid size for the {key} - {value}"
    
        
    return True, "pass"



def validate_form_fields(form = Request.form):
    # Validate each field
    if not form.get('firstname') or not isinstance(form.get('firstname'), str):
        flash('First name is required.', 'error')
        return False
    elif len(form.get('firstname')) < 2 or len(form.get('firstname')) > 50:
        flash('Invalid number of characters in first name. Max character [50]', 'error')
        return False
    
    if not form.get('lastname') or not isinstance(form.get('lastname'), str): 
        flash('Last name is required', 'error')
        return False
    elif len(form.get('firstname')) < 2 or len(form.get('firstname')) > 50:
        flash('Invalid number of characters in first name. Max character [50]', 'error')
        return False
    
    if not form.get('email') or not isinstance(form.get('email'), str):
        flash('Email is required', 'error')
        return False
    elif len(form.get('email')) < 2 or len(form.get('email')) > 30:
        flash('Invalid number of characters in email. Max character [30]', 'error')
        return False



