from flask.views import View
from flask import render_template, redirect, url_for, request, flash, session, jsonify

class ListView(View):
    methods = ['GET']

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        listItems = self.model.list_users()
        return render_template(self.template, items=listItems)