
from flask import Blueprint
from flask_cors import  CORS, cross_origin

bp_courses = Blueprint("course", __name__, url_prefix='/course')
CORS(bp_courses)

from ..token_module.userTokenModel import UserToken
from .enroll.enroll_view import EnrollView
from .course.course import CourseModel
from .enroll.enroll import EnrollModel
from ..package_payment.payment.card_transaction import CardTransactionModel
from ..package_payment.payment.payment_card import PaymentCardModel
from ..package_payment.payment.payment import PaymentModel


bp_courses.add_url_rule("/enroll/<string:course>",view_func=EnrollView.as_view("enroll",EnrollModel, 
CourseModel, UserToken, CardTransactionModel,PaymentModel, PaymentCardModel, "e_learning/enroll_to_course.html"))

