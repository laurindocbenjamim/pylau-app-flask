
import os

from flask import (
    Blueprint, url_for, redirect, session
)

from flask_cors import CORS, cross_origin
from core import db

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
    return redirect(url_for('Auth.two_fa_app_login'))