
from flask import flash, Request
from ..module_sign_up_sub.controller.userController import is_valid_email

def validate_form_fields(form = Request.form):
    # Validate each field
    if not form.get('username') or not isinstance(form.get('username'), str):
        flash('Username is required.', 'error')
        return False
    if is_valid_email(form.get('username')) == False:
        flash('Invalid email address.', 'error')
        return False
    return True