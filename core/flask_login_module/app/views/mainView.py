from flask.views import View
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required


class MainView(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self, template):
        self.template = template

    def dispatch_request(self):
        return render_template(self.template, title="Home", user="John Doe")