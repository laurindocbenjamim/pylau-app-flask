from typing import Any
from flask.views import View
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash

class AuthRegisterView(MethodView):
    methods = ['GET', 'POST']

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        if request.method == 'POST':
            flash('Ready to create a  user', 'success')
                
        flash('Welcome to the user register page', 'error')
        return render_template(self.template, title='Register')
