from typing import Any
from flask.views import View
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash
from ...controller.userController import load_user_obj, validate_user_form

class AuthRegisterView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        if request.method == 'POST':
            if validate_user_form(request.form):                
               
                response = self.model.create_user(load_user_obj(request.form, 'user'))
                if response == 1:
                    flash('User created successfully', 'success')
                    return redirect(url_for('index'))
                else:
                    flash(response, 'error')
                
        return render_template(self.template, title='Register')
