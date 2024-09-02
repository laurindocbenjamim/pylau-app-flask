
from flask import Blueprint
from flask_cors import  CORS, cross_origin

bp_courses = Blueprint("course", __name__, url_prefix='/course')
CORS(bp_courses)

from .enroll_view import EnrollView

bp_courses.add_url_rule("/enroll/<string:course>",view_func=EnrollView.as_view("enroll",None, "e_learning/enroll_to_course.html"))