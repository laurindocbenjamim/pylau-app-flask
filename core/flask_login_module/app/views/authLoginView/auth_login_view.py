import flask
from flask_login import login_user, logout_user
from flask.views import View
from flask import render_template, request, redirect, url_for, flash, jsonify
from .authViewController import validate_user_form

class AuthLoginView(View):
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
                    if user.is_active() == 1:
                        # Use the login_user method to log in the user
                        login_user(user)
                        return redirect(url_for('select.user_list_view'))  
                    logout_user()
                    flask.flash('User is not active', 'error') 
                else:
                    flask.flash('Invalid username or password ', 'error')
            
        return render_template(self.template, title='Login')