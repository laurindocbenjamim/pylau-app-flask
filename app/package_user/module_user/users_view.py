

import traceback
import sys
import os
import flask
from flask_login import login_user, logout_user
from flask_cors import cross_origin
from flask.views import View
from flask import render_template, request, session, redirect, url_for, flash, jsonify,g, make_response

from app.utils.catch_exception_information import _catch_sys_except_information

class UsersView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, userToken, template):
        self.model = model
        self.userToken = userToken
        self.template = template

    @cross_origin(methods=['GET', 'POST'])
    def dispatch_request(self):
        
        user_id = request.args.get('userID',0)

        if request.method == 'GET':
            pass


        response = make_response(render_template(self.template, title="Users"))
        response.set_cookie('current_page', 'admin.users.users_all')
        return response