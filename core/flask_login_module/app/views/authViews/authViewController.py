from flask import flash

def validate_user_form(form):
    if not form.get('username'):
        flash('Username is required', 'error')
        return False
    elif not form.get('password'):
        flash('Password is required', 'error')
        return False
    flash('', '')
    return True