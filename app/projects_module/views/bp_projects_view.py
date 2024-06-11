
from flask import Blueprint
from ..views.projectsView import ProjectsView

bp_project_view = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')
bp_project_view.add_url_rule('/list', view_func=ProjectsView.as_view('list', template='projects.html'))