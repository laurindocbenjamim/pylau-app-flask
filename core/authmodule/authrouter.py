
import os
import functools

from flask import (
    Blueprint, url_for, redirect, session, g
)

from flask_cors import CORS, cross_origin
from core import db, clear_all_sessions
from core import get_user_by_email, get_user_by_id, get_user_by_id_limited_dict

bp = Blueprint("Auth", __name__, url_prefix='/auth')
CORS(bp)

# Importing the route blocks
from core.authmodule.route_blocks._auth_two_fa_app_route import route_two_fa_login
from core.authmodule.route_blocks._auth_route import route_auth
route_auth(bp, db)
route_two_fa_login(bp, db)

# logout route
@bp.route('/logout', methods=['GET'])
@cross_origin(methods=['GET'])
def logout():
    session.clear()
    clear_all_sessions()
    return redirect(url_for('Auth.two_fa_app_login'))


# Load logged in user to verify if the user id is stored in a session
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id_limited_dict(db,user_id) 

    
# REQUIRE A UTHENTICATION IN OTHER VIEWS 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('Auth.two_fa_app_login'))

        return view(**kwargs)

    return wrapped_view