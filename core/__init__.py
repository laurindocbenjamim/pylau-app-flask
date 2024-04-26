
import os
from flask import Flask, jsonify

def create_application(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"sms": "Ola mundo"})

    @app.route('/person/<name>', methods=['GET'])
    def person(name):
        return  f"My name is {name}"

    return app

