

import traceback
import sys
import os


from flask.views import View
from flask_cors import cross_origin
from markupsafe import escape
from flask import render_template, session, request, redirect, url_for, flash, jsonify, make_response, current_app
from werkzeug.utils import secure_filename
from ...configs_package.modules.logger_config import get_message as set_logger_message
from app.utils.catch_exception_information import _catch_sys_except_information
from app.utils.my_file_factory import validate_file, upload_file

from ...configs_package.modules.logger_config import get_message as set_logger_message



class MyLearningView(View):
    """
    
    """
    methods=['GET', 'POST']


    def __init__(self, enroll, course, userToken,template) -> None:
        self._enroll = enroll
        self._userToken = userToken
        self._courseModel = course
        self._template = template

    def dispatch_request(self, course=None):
        course = escape(course)  
        course = str(course).replace('-', ' ')      
        courses = []
        user_id = session.get('user_id', None)
        message = category = ""
        status_code = 200
        course_details = ""
        current_url="course.learn.my_learning"

        if user_id is None or not isinstance(user_id, int) or user_id ==0:
            return redirect(url_for('auth.user.login'))


        status, enroll = self._enroll.get_by_student(student_id = user_id)

        if status:
            if len(enroll)>0:
                for en in enroll:
                    status, mcourse = self._courseModel.get_by_id(course_id=en.course_id)
                    if status:
                        courses.append(mcourse)
    
        response = make_response(render_template(self._template, title="My Learning",current_url=current_url, status=status, my_courses=courses))  
        response.set_cookie('current_page', "course.learn.my_learning")          
        return response
                        
        
        