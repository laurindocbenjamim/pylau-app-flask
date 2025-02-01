
from flask.views import View 
from flask import render_template, redirect, jsonify, request

class StreamAssistent(View):
    methods = ['GET', 'POST']

    def __init__(self, template) -> None:
        self._template = template

    def dispatch_request(self):

        if request.method == 'GET':
            return render_template(self._template, title="sLaur")