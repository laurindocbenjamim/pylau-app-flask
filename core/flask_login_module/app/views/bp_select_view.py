import flask
from flask import Blueprint

from .selectViews.listView import ListView
from ..model.users import Users


"""
This Blueptint is used to integrate the select views into the application
"""
bp = Blueprint('select', __name__, url_prefix='/select')

def init_select_view_app(login_manager):
    
    """
    This function initializes the select views into the application
    """
    bp.add_url_rule('/users/', view_func=ListView.as_view('user_list_view', Users, 'list.html'))
