

from flask import Blueprint
from flask_cors import CORS
from .bp_projects_view import bp_projects
from app.package_data_science.deep_seek_test import DeepSeekAPI
from app.configs_package import csrf, oauth, cache, limiter

bp_data_science = Blueprint('data_science',__name__, url_prefix='/data-science')
CORS(bp_data_science)



from .code_suggestion_openai_view import CodeSuggestionOpenAIView

bp_data_science.add_url_rule("/code-suggestion", view_func=CodeSuggestionOpenAIView.as_view("code_suggestion"))

bp_data_science.register_blueprint(bp_projects)


# Register the view with Flask
deep_seek_view = DeepSeekAPI.as_view("deep_seek_api")
# 🔹 **Disable CSRF for this specific view**


bp_data_science.add_url_rule("/deep-seek/", defaults={"id": None}, view_func=deep_seek_view, methods=["GET"])
bp_data_science.add_url_rule("/deep-seek/", view_func=deep_seek_view, methods=["POST"])
bp_data_science.add_url_rule("/deep-seek/<string:id>", view_func=deep_seek_view, methods=["GET", "PUT", "DELETE"])