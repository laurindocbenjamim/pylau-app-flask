import requests
import os
from flask import Flask, render_template, jsonify, url_for, request

def create_app(test_config=None):
    # Create and configure the app
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
        DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load  the  instance config if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
       
    else:
        # Load the test config if passed in
        application.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    @application.route('/')
    def index():
        return render_template('index.html')
   
    # Simple page that say hello
    @application.route("/test")
    def hello():
        return "<h2>Hello, this a test </h2>"
    
    return application