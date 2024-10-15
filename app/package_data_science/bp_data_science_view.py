
import requests
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .bp_projects_view import bp_projects

bp_data_science = Blueprint('data_science',__name__, url_prefix='/data-science')
CORS(bp_data_science)



from .code_suggestion_openai_view import CodeSuggestionOpenAIView

bp_data_science.add_url_rule("/code-suggestion", view_func=CodeSuggestionOpenAIView.as_view("code_suggestion"))

bp_data_science.register_blueprint(bp_projects)

@bp_data_science.route('/ttst')
def ttt():
    return f"OLlla"