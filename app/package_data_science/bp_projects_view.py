
from flask import Blueprint, session
from flask_cors import CORS
from ..token_module import UserToken
from ..auth_package import Users
from .module_sentiment_analyse.sentiment_analyse_view import SentimentAnalyseView

bp_projects = Blueprint('project', __name__, url_prefix='/project')
CORS(bp_projects)
bp_projects.add_url_rule('/sentiment-analyse/<string:user_token>', view_func=SentimentAnalyseView.as_view('sentiment_analyse', UserToken, Users, 'package_data_science/sentiment_analyse.html'))
