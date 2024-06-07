from flask import Blueprint
from . mainView import MainView

bp = Blueprint('main_view', __name__, template_folder='templates')

bp.add_url_rule('/', view_func=MainView.as_view('main_view', 'home.html'))