from flask import Blueprint
from . mainView import MainView

bp = Blueprint('main_view', __name__, template_folder='templates')

""" Here I integrate a view that is a class that inherits from the View class
 to the blueprint. The view is the main view of the application and is the first
    view that the user sees when they open the application.

 """

bp.add_url_rule('/', view_func=MainView.as_view('main_view', 'home.html'))