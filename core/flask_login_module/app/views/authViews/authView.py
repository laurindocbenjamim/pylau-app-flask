from flask_login import login_user
from flask.views import View
from flask import render_template, request, redirect, url_for, flash
from .authViewController import validate_user_form

class AuthView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        if request.method == 'POST':
            if validate_user_form(request.form):
                username = request.form.get('username')
                password = request.form.get('password')
                user = self.model.query.filter_by(username=username).first()
                
                if user and user.check_password(password):
                    # Use the login_user method to log in the user
                    login_user(user)
                    return redirect(url_for('create'))
                else:
                    flash('Invalid username or password', 'error')
            
        return render_template(self.template, title='Login')