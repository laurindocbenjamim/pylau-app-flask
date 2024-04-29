
import os
from flask import (
    Flask, jsonify, render_template
)

def create_application(test_config=None):
    app = Flask(__name__, static_folder="static", static_url_path="static", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    from . modules.codeskill import dictionaries
    app.register_blueprint(dictionaries.bpapp)


    @app.route('/api', methods=['GET', 'POST'])
    def api():
        return render_template('fetchapi/api.html')

    @app.route('/', methods=['GET'])
    def index():
        return  render_template('index.html')

    @app.route('/person/<name>', methods=['GET'])
    def person(name):
        return  f"My name is {name}"
    
    @app.route('/blog', methods=['GET'])
    def blog():
        return  render_template('index.html')

    return app

