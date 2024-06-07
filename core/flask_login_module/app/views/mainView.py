from flask.views import View
from flask import render_template, request, redirect, url_for, flash

class MainView(View):
    methods = ['GET', 'POST']

    def __init__(self, template):
        self.template = template

    def dispatch_request(self):
        return render_template(self.template, title="Home", user="John Doe")