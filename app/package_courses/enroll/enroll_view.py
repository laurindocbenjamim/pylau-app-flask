

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
from .controller import validate_words#, validate_file
from ...configs_package.modules.logger_config import get_message as set_logger_message
from .controller import create_payment_objects





class EnrollView(View):
    """
    
    """
    methods=['GET', 'POST']

    course_codes = ["PB002401", "PB002403"]

    def __init__(self, enroll, course, userToken, cardTransaction, 
                 payment, paymentCard ,template) -> None:
        self._enroll = enroll
        self._userToken = userToken
        self._courseModel = course
        self._cardTransaction = cardTransaction
        self._paymentCard = paymentCard
        self._payment = payment
        self._template = template

    def dispatch_request(self, course=None):
        course = escape(course)  
        #course = str(course).replace('', ' ')   
        course_id= request.args.get('course_id', 0)   
        message = category = ""
        status_code = 400
        student_id = session.get('user_id', '')
        course_details = ""
        status = False
    
        # Method to validate the form fields
        def is_form_valid():
            _message = _category ='' 
            for key, value in request.form.items():
                status, sms = validate_words(key=key, value=value)
                if not status:
                    _message = f'{sms}'
                    _category = "error"
                    break
            return status, _message, _category

        #secure = MySecureUtils()       
        
        """ First chet  if there is a user token if not rediret the user to the login page
        """
        def check_token():
            if 'user_token' in session or session.get('user_token') is not None or session.get('user_token') !='':
                if self._userToken.is_user_token_expired(session.get('user_token')):
                    session.clear()    
                    #request.cookies.add('preview_url', request.url)             
                    return redirect(url_for('auth.user.login'))
            else:
                return redirect(url_for('auth.user.login'))
            
           

        if request.method == 'GET':   

            # Render the template and then set a cookie
            response = make_response(render_template(self._template, title="Enroll to Python Basic", course=str(course).upper(), course_code=course_id))            
            return response
         
            # First check the user token
            check_token()    

            if not student_id or student_id is None or student_id =='':
                return redirect(url_for('auth.user.login'))

            status, resp = self._enroll.check_if_student_enrolled(student_id=student_id, course_id=course_id)
            if status:
                return redirect(url_for('course.learn.my_learning', token=session.get('user_token'))) 
            
            # Render the template and then set a cookie
            response = make_response(render_template(self._template, title="Enroll to Python Basic", course=str(course).upper(), course_code=course_id))            
            return response
        
            """
            Below we catch the POST method request
            """
        elif request.method == 'POST':
            # First check the user token
            check_token()

            """
            Gets the cookie from the user request, a token previously 
            passed, check if it is expired. 
            If true redirect the user to the login page.
            """
            user_cookie = request.cookies.get('user_cookie')
                
            if self._userToken.is_user_token_expired(session.get('user_token')):
                session.clear()                
                return redirect(url_for('auth.user.login'))
            
            try:                
                
                # Validate the form fields
                status, message, category = is_form_valid()
                
                if not status:
                    flash(message, "error") 
                else:
                    file_field_name='bankTicket'
                    # check if the payment method is by ticket bank
                    if request.form.get('paymentMethod') == 'bank reference':
                        status, message = validate_file(request=request, file_field_name=file_field_name)
                    
                        if not status:
                            flash(message, "error") 
                        else:
                            #file = request.files[f'{file_field_name}']
                            #
                            status, filename = upload_file(request_file=request.files, file_field_name=file_field_name)

                            if not status: 
                                flash(f"Failed to upload file. {status}", "error")
                            else:
                                status, enroll_obj, card_obj, payment_obj = create_payment_objects(
                                    request.form,
                                    user_id=session['user_id'],
                                    filename = filename                                   
                                )
                                                            
                                status,_str= self._cardTransaction.execute_transaction(
                                    enroll_obj = enroll_obj, 
                                    card_obj = card_obj, 
                                    payment_obj = payment_obj
                                )
                                if not status:
                                    flash(_str, 'error')
                                else:   
                                    status_code=200
                                    flash(f"Ready to study {status}-{_str}", "success")
                                  
                    else:
                        
                        status, enroll_obj, card_obj, payment_obj = create_payment_objects(
                            request.form, 
                            user_id=session['user_id']                           
                        )                        
                        
                        status,_str= self._cardTransaction.execute_transaction(
                            enroll_obj = enroll_obj, 
                            card_obj = card_obj, 
                            payment_obj = payment_obj
                        )
                        if not status:
                            flash(_str, 'error')
                        else:   
                            status_code=200
                            flash(f"Ready to study {status}-{_str}", "success")

            except Exception as e:
                custom_message = "General error in Enrollment of course."
                error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="ENROLL COURSE", custom_message=custom_message)
                set_logger_message(error_info)
                flash(str(e), 'error')
                return f" {str(e)}", ""
            finally:   
                if status_code==200:
                    return redirect(url_for('course.learn.my_learning', token=session.get('user_token')))             
                response = make_response(render_template(self._template, title="Enroll to Python Basic", course=str(course).upper(), course_code=course_id))            
                return response
                        
        
        