import re
from flask import flash, Request

def validate_form_fields(form = Request.form):
    # Validate each field
   
    if not form.get('username') or not isinstance(form.get('username'), str):
        flash('Email or username is required', 'error')
        return False
    elif len(form.get('username')) < 2 or len(form.get('username')) > 30:
        flash('Invalid number of characters in username. Max character [30]', 'error')
        return False
    
    if is_valid_email(form.get('username')) == False:
        flash('Invalid username address.', 'error')
        return False
    
    
    if not form.get('password') or not isinstance(form.get('password'), str):
        flash('Password is required', 'error')
        return False
    
    # Filter unauthorized characters
    authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    authorized_integer = "0123456789"
    authorized_country_code_chars = "0123456789+"
    authorized_password_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_!@#$%^&*()_+"

    if any(char not in authorized_password_chars for char in form.get('password')):
        flash('Invalid characters in password', 'error')
        return False
            
    if is_strong_password(form.get('password')) == False:
        flash('Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character', 'error')
        return True
    
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
