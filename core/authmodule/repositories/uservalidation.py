import re

def validate_form_fields(firstname, lastname, email, country,
            country_code, phone, password, confirm, two_factor_auth_code):
        # Validate each field
        if not firstname or not isinstance(firstname, str):
            message = 'First name is required'
            status = False
            return status, message
        if not lastname or not isinstance(lastname, str):
            message = 'Last name is required'
            status = False
            return status, message
        if not email or not isinstance(email, str):
            message = 'Email is required'
            status = False
            return status, message
        if not country or not isinstance(country, str):
            message = 'Country is required'
            status = False
            return status, message
        if not country_code or not isinstance(country_code, str):
            message = 'Country code is required'
            status = False
            return status, message
        if not phone or not isinstance(phone, str):
            message = 'Phone is required'
            status = False
            return status, message
        if not two_factor_auth_code or not isinstance(two_factor_auth_code, str):
            message = 'Two-factor authentication code is required'
            status = False
            return status, message
        if not password or not isinstance(password, str):
            message = 'Password is required'
            status = False
            return status, message
        if not confirm or not isinstance(confirm, str):
            message = 'Confirm password is required'
            status = False
            return status, message

        # Filter unauthorized characters
        authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        authorized_integer = "0123456789"
        if any(char not in authorized_chars for char in firstname):
            message = 'Invalid characters in first name'
            status = False
            return status, message
        if any(char not in authorized_chars for char in lastname):
            message = 'Invalid characters in last name'
            status = False
            return status, message
        if any(char not in authorized_chars for char in country):
            message = 'Invalid characters in country'
            status = False
            return status, message
        if any(char not in authorized_chars for char in country_code):
            message = 'Invalid characters in country code'
            status = False
            return status, message
        if any(char not in authorized_integer for char in phone):
            message = 'Invalid characters in phone'
            status = False
            return status, message
        if any(char not in authorized_chars for char in two_factor_auth_code):
            message = 'Invalid characters in two-factor authentication code'
            status = False
            return status, message
        if any(char not in authorized_chars for char in password):
            message = 'Invalid characters in password'
            status = False
            return status, message
        if any(char not in authorized_chars for char in confirm):
            message = 'Invalid characters in confirm password'
            status = False
            return status, message

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
