import re
from flask import flash, Request


"""
 This module contain the global funtios/methods to validate 
 form fields such as general strings or passwords, emails and 
 other specific charcters

"""

def validate_only_str(s):
        # This pattern allows spaces, accentuated characters, and common punctuation
        pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\'"()]+$'
        if re.match(pattern, s):
            return True
        else:
            return False
        

def validate_str_and_punct_char(s):
    # This pattern allows spaces, accentuated characters, and common punctuation
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s.,;!?\'"()]+$'
    if str(s) != '':
        if not  re.match(pattern, s):
            return False
    return True

def validate_str_digits(s):
    # This pattern allows spaces, accentuated characters, digits
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\'"()]+$'
    if str(s) != '':
        if not  re.match(pattern, s):
            return False
    return True
        
def validate_str_punct_and_digits(s):
    # This pattern allows spaces, accentuated characters, numbers, and common punctuation
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,;!?\'"()]+$'
    if str(s) != '':
        if not  re.match(pattern, s):
            return False
    return True

# Validate password strength
def is_strong_password(password) -> bool:
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
def is_valid_email(email) -> bool:
    if not email:
        return False
    elif not isinstance(email, str):
        return False

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, email) is not None:
        domain = email.split('@')[1]
        if domain.endswith('gmail.com') or domain.endswith('outlook.com') or domain.endswith('hotmail.com') or domain.endswith('live.com') or domain.endswith('icloud.com'):
            return True
    return False
