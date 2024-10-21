

import json
import os
import stat
import ast

from flask import Blueprint, render_template, session, request, make_response, jsonify, current_app, redirect, url_for
from flask_cors import CORS, cross_origin
from markupsafe import escape

bp_learn = Blueprint("learn", __name__, url_prefix="/learn")
CORS(bp_learn)

from ..token_module.userTokenModel import UserToken
from ..package_courses.enroll.enroll_view import EnrollView

from ..package_courses.course.course import CourseModel
from ..package_courses.enroll.enroll import EnrollModel
from ..package_courses.content.courses_content import CourseContentModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel

from .elearning.my_learning_view import MyLearningView
bp_learn.add_url_rule("/my-learning", view_func=MyLearningView.as_view("my_learning",EnrollModel, CourseModel, UserToken, "e_learning/my-learning.html"))

from .elearning.study_this_course_view import StudyThisCourseView
bp_learn.add_url_rule("/this/<string:course>", view_func=StudyThisCourseView.as_view("this_course",CourseContentModel, CourseModel, UserToken, 'e_learning/courses_content/python_courses/study-this-course.html'))


#
@bp_learn.route('/laubcode-editor')
@cross_origin(methods=['GET'])
def laubcode():
    user_id = session.get('user_id', None)
    course_id = request.args.get('userID')
    course_content = {}

    response = make_response(render_template('e_learning/code_editor/my_code_editor.html', title="LAUBCode"))
    from ..utils.config_headers import set_header_params
    set_header_params(response)
    response.set_cookie('current_page', "course.learn.laubcode") 
    return response

@bp_learn.route('/python-basic')
@cross_origin(methods=['GET'])
def python_basic():
    user_id = session.get('user_id', None)
    course_id = request.args.get('courseID')
    course_content = []
    modules = []
    modules_content = []
    
    if user_id is None or user_id =='':
        return redirect(url_for('auth.user.login'))
    else:
        cc_model = CourseContentModel
        status, course_content = cc_model.get_content_by_course_id(course_id=course_id)
        contents = cc_model.convert_to_list(course_content)

        if contents and status and len(contents) > 0:
            for obj in contents:
                if obj['content_module'] not in modules:
                    modules.append(int(obj['content_module']))

        #return jsonify({"modules": modules, "contents": contents, "status": [True  if int(c.content_module)  == modules[0] else False for c in course_content]
        #                , "module": modules[0] == 1 })
    response = make_response(render_template('e_learning/courses_content/python_courses/python-basic.html', 
                                             title="Python Basic", course_id=course_id, course="Python Basic",  course_content=course_content, modules=modules, current_url="course.learn.python_basic"))
    from ..utils.config_headers import set_header_params
    set_header_params(response)
    response.set_cookie('current_page', "course.learn.python_basic") 
    return response

@bp_learn.route('/python-basic/get/<int:courseID>')
@cross_origin(methods=['GET'])
def python_basic_get(courseID):
    user_id = session.get('user_id', None)
    course_id = escape(courseID) #request.args.get('courseID')
    course_content = []
    modules = []
    modules_content = []
    
    if user_id is not None and user_id !='':
        dd = []
        cc_model = CourseContentModel
        status, course_content = cc_model.get_content_by_course_id(course_id=course_id)
        return jsonify({"content": cc_model.convert_to_list(course_content)})
    return jsonify({"content": []})

@bp_learn.route('/notes/new/<int:courseID>/<string:lesson>', methods=['POST'])
@cross_origin(methods=['POST'])
def save_my_notes(courseID, lesson):
    user_id = session.get('user_id', None)
    lesson = escape(lesson)
    course_id = escape(courseID) #request.args.get('courseID')
   
    comment = request.form.get('comment', None)
    lesson = request.form.get('lesson', None)

    from datetime import datetime, timezone
    from ..package_comments.study_notes import StudyNotes
    

    file_path = f'/user_notes/user{user_id}_c{course_id}_{str(lesson).lower().replace(' ', '_')}.json'
    
    new_comment = {
        'user': user_id,
        'course_id': course_id,
        'comment': comment,
        'lesson': lesson,
        'timestamp': datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    }
    
    st, resp = StudyNotes(file_path=file_path, file_directory='/user_notes')\
        .add_comment(new_comment=new_comment)
    #Remove write permissions
    #os.chmod(file_path, stat.S_IREAD)
    
    return jsonify({"status": st, "sms": resp}, 200)

@bp_learn.route('/notes/get/<int:courseID>/<string:lesson>', methods=['GET'])
@cross_origin(methods=['GET'])
def get_my_notes(courseID, lesson):
    user_id = session.get('user_id', None)
    lesson = escape(lesson)
    course_id = escape(courseID) #request.args.get('courseID')
   
    from ..package_comments.study_notes import StudyNotes
    

    file_path = f'/user_notes/user{user_id}_c{course_id}_{str(lesson).lower().replace(' ', '_')}.json'
    
    # Set permissions (read, write, execute for owner; read, execute for group and others)
    #os.chmod(current_app.config['UPLOAD_FOLDER']+'/user_notes', 0o755) 
    #os.chmod(current_app.config['UPLOAD_FOLDER']+file_path, 0o644) 
    
    resp = StudyNotes(file_path=file_path, file_directory='/user_notes').load_comments()

    #Remove write permissions
    #os.chmod(current_app.config['UPLOAD_FOLDER']+file_path, stat.S_IREAD)
    
    return jsonify({"status": True, "notes": resp }, 200)


@bp_learn.route('/python-for-data-visualize')
@cross_origin(methods=['GET'])
def python_for_data_visualize():
    current_url="course.learn.python_basic"
    return f"Python for Data visualization"



