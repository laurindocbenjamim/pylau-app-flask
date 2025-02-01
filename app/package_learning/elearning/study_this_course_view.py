

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



class StudyThisCourseView(View):
    """
    
    """
    methods=['GET', 'POST']


    def __init__(self, course, courseContent, userToken,template) -> None:
        self._courseContent = courseContent
        self._userToken = userToken
        self._courseModel = course
        self._template = template

    def dispatch_request(self, course):
        course = escape(course).replace('-', ' ')  
        #course = str(course).replace('-', ' ')      
        user_id = session.get('user_id', None)
        course_id = request.args.get('courseID')
        course_content = []
        modules = []

        if user_id is None or user_id =='':
            return redirect(url_for('auth.user.login'))
        else:
            status, course_content = self._courseModel.get_content_by_course_id(course_id=course_id)
            contents = self._courseModel.convert_to_list(course_content)

            if contents and status and len(contents) > 0:
                for obj in contents:
                    if obj['content_module'] not in modules:
                        modules.append(int(obj['content_module']))
    
        response = make_response(render_template(self._template, 
                                             title=course, course_id=course_id, course=course, course_content=course_content, modules=modules, current_url="course.learn.this_course"))
        from ...utils.config_headers import set_header_params
        set_header_params(response)
        response.set_cookie('current_page', "course.learn.this_course") 
        return response
                        
        
        