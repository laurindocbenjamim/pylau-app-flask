import requests
import os
from flask import Flask, render_template, jsonify, url_for, request



def create_application(test_config=None):
    # Create and configure the app
    application = Flask(__name__, instance_relative_config=True)
    
    
    
    
    # Import modules
    #from .modules.codeskills import dictionaries
    #application.register_blueprint(dictionaries.bpapp)
    

    @application.route('/')
    def index():
        #return render_template('index.html')
        return jsonify({"message": "Ola Mundo"})
   
    # Simple page that say hello
    @application.route("/test")
    def hello():
        return "<h2>Hello, this a test </h2>"
    
   
    
    return application