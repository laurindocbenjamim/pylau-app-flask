from flask import Blueprint
from .registFormView import RegistFormView

bp = Blueprint('form', __name__, url_prefix='/form')
bp.add_url_rule('/regist', view_func=RegistFormView.as_view('regist', template='form.html'))