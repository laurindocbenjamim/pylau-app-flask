from typing import Any
from flask.views import View
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, jsonify
from ..controller.userController import load_user_obj, validate_form_fields

class AuthRegisterView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        if request.method == 'POST':

            # Validate form fields
            if validate_form_fields(request.form):                

                # Check if email exists
                if self.model.check_email_exists(request.form.get('email')):
                    flash('Email already exists', 'info')
                
                # Check if phone exists
                elif self.model.check_phone_exists(request.form.get('phone')):
                    flash('Phone already exists', 'info')

                # If email and phone do not exist, create user
                else:
                    response = self.model.create_user(load_user_obj(request.form, 'user'))
                    if response == 1:
                        flash('User created successfully', 'success')
                        return redirect(url_for('index'))
                    else:
                        flash(response, 'error')
                
                
        return render_template(self.template, title='Register')
