
import os
from flask import (
    Flask, jsonify, render_template, url_for, request, json
)

def create_application(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    from . modules.codeskill import dictionaries
    app.register_blueprint(dictionaries.bpapp)

    from . modules.authmodule import auth
    app.register_blueprint(auth.bpapp)


    @app.route('/api', methods=['GET', 'POST'])
    def api():
        return render_template('fetchapi/api.html')

    @app.route('/', methods=['GET'])
    def index():
        return  render_template('home.html')

    @app.route('/home', methods=['GET'])
    def home():
        return render_template('laurindo-c-benjamim.html')

    @app.route('/person', methods=['GET', 'POST'])
    def person():
        peoples=[]
        
        if request.method =='GET':            
            return jsonify({"object": peoples})
        if request.method == 'POST':
            code = request.form['code']
            peoples.append({"name": "new", "age": code})
            return jsonify({"object": peoples})
    
    @app.route('/laurindo', methods=['GET'])
    def blog():
        return jsonify({"msms": 1222})

    return app

