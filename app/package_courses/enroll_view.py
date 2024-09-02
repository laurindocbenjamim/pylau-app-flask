

import traceback
import sys
import os
from flask.views import View
from flask_cors import cross_origin
from markupsafe import escape
from flask import render_template, session, request, redirect, url_for, flash, jsonify

from ..configs_package.modules.logger_config import get_message as set_logger_message
from app.utils.catch_exception_information import _catch_sys_except_information


class EnrollView(View):
    #@cross_origin(['GET', 'POST'])
    methods=['GET', 'POST']

    def __init__(self, model, template) -> None:
        self._model = model
        self._template = template

    def dispatch_request(self, course=None):

        if 'user_token' in session:
            if self.userToken.is_user_token_expired(session['user_session']):
                session.clear()                
                return redirect(url_for('auth.user.login'))

        if request.method == 'POST':
            return render_template(self._template, title=f"Enroll to {course}")
        return render_template(self._template, title=f"Enroll to {course}")