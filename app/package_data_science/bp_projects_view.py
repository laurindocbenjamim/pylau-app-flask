
from flask import Blueprint, session
from flask_cors import CORS
from ..token_module import UserToken
from ..auth_package import Users
from .module_sentiment_analyse.emotion_detector_view import EmotionDetectorView
from .module_sentiment_analyse.emotion_detector import EmotionDetector

bp_projects = Blueprint('project', __name__, url_prefix='/project')
CORS(bp_projects)
bp_projects.add_url_rule('/emotion-detector/<string:user_token>', view_func=EmotionDetectorView.as_view('emotion_detector', UserToken, Users, EmotionDetector, 'package_data_science/emotion_detector.html'))
