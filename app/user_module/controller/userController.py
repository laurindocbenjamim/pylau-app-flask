from ..model.users import Users
from flask import flash, Request
from werkzeug.security import generate_password_hash

def load_user_obj(form = Request.form, role='user'):
    return Users(
        username = form.get('username'), 
        password = generate_password_hash(form.get('password')), 
        email = form.get('email'), 
        role = role
        )
        


def validate_user_form(form):
    if not form.get('username'):
        flash('Username is required', 'error')
        return False
    elif not form.get('email'):
        flash('Email is required', 'error')
        return False
    elif not form.get('password'):
        flash('Password is required', 'error')
        return False
    flash('', '')
    return True

def validate_login_form(form):
    if not form.get('email'):
        flash('Email is required', 'error')
        return False
    elif not form.get('password'):
        flash('Password is required', 'error')
        return False
    flash('', '')
    return True