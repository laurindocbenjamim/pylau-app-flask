from flask.views import View
from flask import render_template, redirect, url_for, request, flash, session, jsonify

class HomeView(View):
    def dispatch_request(self):
        return "Hello, World!"