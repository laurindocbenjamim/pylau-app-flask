
from flask import (
    Blueprint, jsonify, url_for
)

bp = Blueprint("Dictionaries", __name__, url_prefix='/xcode')

@bp.route('/dictionaries')
def person1():
    person1={"name": "Laurindo", "age": 23}
    n,d,f=12,11,14
    return jsonify({"list": person1, "number":n+d+f})