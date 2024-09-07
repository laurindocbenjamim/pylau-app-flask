

import traceback
import sys
import os


from flask.views import View
from flask_cors import cross_origin
from markupsafe import escape
from flask import render_template, session, request, redirect, url_for, flash, jsonify, make_response, abort
from ...configs_package.modules.logger_config import get_message as set_logger_message
from app.utils.catch_exception_information import _catch_sys_except_information
from .controller import validate_form
from app.configs_package import MySecureUtils


class EnrollView(View):
    """
    
    """
    methods=['GET', 'POST']

    def __init__(self, enroll, courseModel, userToken ,template) -> None:
        self._enroll = enroll
        self._userToken = userToken
        self._courseModel = courseModel
        self._template = template

    def dispatch_request(self, course=None):
        course = escape(course)
        message = ""
        category = ""

        #secure = MySecureUtils()       
        
        """ First chet  if there is a user token if not rediret the user to the login page
        """
        
        if 'user_token' in session:
            if self._userToken.is_user_token_expired(session.get('user_token')):
                session.clear()                
                return redirect(url_for('auth.user.login'))
        else:
            return redirect(url_for('auth.user.login'))

        if request.method == 'GET':            
            
            # Render the template and then set a cookie
            response = make_response(render_template(self._template, title="Enroll to Python Basic", course="Python Basic", course_code="PB002401"))
            
            return response
        
        
            """
            Below we catch the POST method request
            """
        elif request.method == 'POST':

            """
            Gets the cookie from the user request, a token previously 
            passed, check if it is expired. 
            If true redirect the user to the login page.
            """

            user_cookie = request.cookies.get('user_cookie')
           
            if self._userToken.is_user_token_expired(session.get('user_token')):
                session.clear()                
                return redirect(url_for('auth.user.login'))
            if validate_form(request.form):
                flash("Ready to study", "success")            

            response = make_response(render_template(self._template, title="Enroll to Python Basic", course="Python Basic", course_code="PB002401"))
            
            return response
                        
        
        