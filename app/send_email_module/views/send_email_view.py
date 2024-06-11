
from flask.views import View
from flask import render_template, redirect, url_for, request, flash,jsonify
from flask_login import login_required
#from flask_caching import cache

class SendEmailView(View):
    decorators = [login_required]
  
    init_every_request = True
    methods = ['GET']

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        listItems = [
            {
                "code": "1",
            "name": "Project 1",
            "description": "Description 1",
        }
        ]
        return render_template(self.template, title="LSend email", items=listItems)