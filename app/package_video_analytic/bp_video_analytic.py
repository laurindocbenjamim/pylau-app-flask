from app.dependencies import Blueprint
from app.dependencies import render_template
from app.dependencies import make_response
from app.dependencies import CORS
from app.dependencies import cross_origin

bp_video_analytic = Blueprint('bp_video_analytic', __name__, url_prefix='/video-analytic')
CORS(bp_video_analytic)

@bp_video_analytic.route('/get-video-analytic', methods=['GET'])
@cross_origin(methods=['GET'])
def get_video_analytic():
    response = make_response(
        render_template(
            "video_analytic/video_upload.html",
            title="Upload Video"
            ))
    return response