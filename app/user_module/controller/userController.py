import re
from ..model.users import Users

from flask import flash, Request
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

def load_user_obj(form = Request.form, role='user', active=0):
    return Users(
        firstname = form.get('firstname'),
        lastname = form.get('lastname'),
        email = form.get('email'),
        country = form.get('country'),
        country_code = form.get('country_code'),
        phone = form.get('phone'),
        password = generate_password_hash(form.get('password')),        
        role = role,
        active = active
        )
        




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
    
    if is_valid_email(form.get('email')) == False:
        flash('Invalid email address.', 'error')
        return False
    
    if not form.get('country') or not isinstance(form.get('country'), str):
        flash('Country is required', 'error')
        return False
    elif len(form.get('country')) < 2 or len(form.get('country')) > 50:
        flash('Invalid number of characters in country. Max character [50]', 'error')
        return False
    
    if not form.get('country_code') or not isinstance(form.get('country_code'), str):
        flash('Country code is required', 'error')
        return False
    elif len(form.get('country_code')) < 1 or len(form.get('country_code')) > 5:
        flash('Invalid number of digits in country code. Max character [5]', 'error')
        return False
    
    if not form.get('phone') or not isinstance(form.get('phone'), str):
        flash('Phone is required', 'error')
        return False
    elif len(form.get('phone')) < 9 or len(form.get('phone')) > 15:
        flash('Invalid number of digits in phone. Max character [15]', 'error')
        return False
    
    if not form.get('two_fa_auth_method') or not isinstance(form.get('two_fa_auth_method'), str):
        flash('Two-factor authentication code is required', 'error')
        return False
    if not form.get('password') or not isinstance(form.get('password'), str):
        flash('Password is required', 'error')
        return False
    if not form.get('confirm') or not isinstance(form.get('confirm'), str):
        flash('Confirm password is required', 'error')
        return False
        
    if str(form.get('password')) != str(form.get('confirm')):
        flash('The passwords do not match', 'error')
        return False

    # Filter unauthorized characters
    authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    authorized_integer = "0123456789"
    authorized_country_code_chars = "0123456789+"
    authorized_password_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_!@#$%^&*()_+"


    # Validate each field
    if any(char not in authorized_chars for char in form.get('firstname')):
        flash('Invalid characters in first name', 'error')
        return False
    
    # Validate each field
    if any(char not in authorized_chars for char in form.get('lastname')):
        flash('Invalid characters in last name', 'error')
        return False
    
    if any(char not in authorized_chars for char in form.get('country')):
        flash('Invalid characters in country', 'error')
        return False
    
    if any(char not in authorized_country_code_chars for char in form.get('country_code')):
        flash('Invalid characters in country code', 'error')
        return False
    
    
    if any(char not in authorized_integer for char in form.get('phone')):
        flash('Invalid characters in phone', 'error')
        return False
    
    
    if any(char not in authorized_password_chars for char in form.get('password')):
        flash('Invalid characters in password', 'error')
        return False
    if any(char not in authorized_password_chars for char in form.get('confirm')):
        flash('Invalid characters in confirm password', 'error')
        return False
        
    if is_strong_password(form.get('confirm')) == False:
        flash('Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character', 'error')
        return False
    # Return true if all fields are valid
    return True



# Validate password strength
def is_strong_password(password):
    if not password or not isinstance(password, str):
        return False

    # Check password length
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check for at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # Check for at least one special character
    special_chars = "!@#$%^&*()_+"
    if not any(char in special_chars for char in password):
        return False

    return True
# Validate email
def is_valid_email(email):
    if not email or not isinstance(email, str):
        return False

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, email) is not None:
        domain = email.split('@')[1]
        if domain.endswith('gmail.com') or domain.endswith('outlook.com') or domain.endswith('hotmail.com') or domain.endswith('live.com') or domain.endswith('icloud.com'):
            return True
    return False
