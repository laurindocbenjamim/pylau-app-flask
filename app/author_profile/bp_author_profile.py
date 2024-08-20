
from flask import Blueprint,  render_template, redirect, jsonify
from flask_cors import CORS, cross_origin

bp_author = Blueprint('profile', __name__, url_prefix='/profile')
CORS(bp_author)

@bp_author.route('/')
@cross_origin(methods=['GET'])
def author_profile():
    return render_template('author_profile/index.html')
from .author_profile_view import AuthorProfileView

bp_author.add_url_rule("/laurindo-c-benjamim.html", view_func=AuthorProfileView.as_view('laurindo_c_benjamim', 'author_profile/about-laurindo-c-benjamim.html'))