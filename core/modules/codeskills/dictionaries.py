
from flask import (
    Blueprint, jsonify
)

bpapp = Blueprint("Dictionaries", __name__, url_prefix='/xcode')

@bpapp.route('/dictionaries')
def person1():
    person1={"name": "Laurindo", "age": 23}
    n,d,f=12,11,14
    return jsonify({"list": person1, "number":n+d+f})