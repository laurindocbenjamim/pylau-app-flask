

import traceback
import sys
import os


from flask.views import View
from flask_cors import cross_origin
from markupsafe import escape
from flask import render_template, session, request, redirect, url_for, flash, jsonify, make_response, current_app
from werkzeug.utils import secure_filename
from ..content.controller import validate_words, create_dict

from ...configs_package.modules.logger_config import get_message as set_logger_message
from app.utils.catch_exception_information import _catch_sys_except_information
from app.utils.my_file_factory import validate_file, upload_file

from ...configs_package.modules.logger_config import get_message as set_logger_message



class CourseContentPostUpdateView(View):
    """
     
    """
    methods=['GET', 'POST']


    def __init__(self, courseContent, userToken,USER_DATA,template) -> None:
        self._userToken = userToken
        self._courseContent = courseContent
        self._template = template
        self.USER_DATA = USER_DATA

    def dispatch_request(self):
        
        course_id = escape(request.args.get('courseID'))
        description = escape(request.args.get('description'))

        # Method to validate the form fields
        def is_form_valid():
            _message = _category ='' 
            for key, value in request.form.items():
                status, sms = validate_words(key=key, value=value)
                if not status:
                    _message = f'{sms}'
                    _category = "text-danger"
                    break
            return status, _message, _category
        
        if request.method =='POST':
            # Validate the form fields
            
            status, message, category = is_form_valid() 
            if not status:
                flash(message=message, category=category)
            else:
                
                file_field_name='thumbnail'
                filename = ''

                if f'{file_field_name}' in request.files:
                
                    file = request.files[f'{file_field_name}']

                    if file.filename != '':
                    # Validate the thumbnail file                  
                        status, message = validate_file(request=request, file_field_name=file_field_name)

                        if not status:
                            flash(message=message, category='text-danger')
                        else:
                            status, filename = upload_file(request_file=request.files, file_field_name=file_field_name, folder='thumbnail')
                
                
                dict_of_obj = create_dict(request.form, filename=filename)
                
                status, obj = self._courseContent.create(course=dict_of_obj)
                if not status:                  
                    flash(obj, category='text-danger')
                else:
                    return redirect(url_for('course.get_all'))
        
        from ...utils import set_header_params               
        response = make_response(render_template(self._template, USER_DATA=self.USER_DATA, courseID=course_id, description=description, title="New course content"))
        response.set_cookie('current_page', "course.content_post")
        
        set_header_params(response)
        return response



