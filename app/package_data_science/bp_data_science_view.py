
from flask import Blueprint
from flask_cors import CORS
from .bp_projects_view import bp_projects

bp_data_science = Blueprint('data_science',__name__, url_prefix='/data-science')
CORS(bp_data_science)
bp_data_science.register_blueprint(bp_projects)