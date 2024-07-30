


import os
import secrets
from flask import Flask, current_app, request, session, jsonify, render_template
from flask_cors import CORS, cross_origin

from flask_migrate import Migrate
from flask_login import LoginManager
from .configs_package import DevelopmentConfig, TestingConfig, ProductionConfig

from .configs_package.modules.load_database import db


"""

"""
def create_app(JDBC="sqlite",test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
  
    CORS(app)

    if test_config is None:
        # Load  the  instance config if it exists, when not testing
        #app.config.from_pyfile('config.py', silent=True)
        app.config.from_object(DevelopmentConfig(JDBC))
    else:
        # Load the test config if passed in
        #app.config.from_mapping(test_config)
        app.config.from_object(TestingConfig())

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Login Manager is needed for the the application 
    # to be able to log in and log out users

    login_manager = LoginManager()
    login_manager.init_app(app)
    #login_manager.login_view = 'auth.user.login'

    # import and call the database configuration
    from app.configs_package.modules.load_database import init_db_server  
    init_db_server(app)

    #from .routes import load_routes
    #from .configs_package.views.routes import load_routes
    from .utils.views.routes import load_routes
    load_routes(app=app, db=db, login_manager=login_manager)
    
    

    # Simple page that say hello
    @app.route("/hello")
    def hello():
        return 'Hello, World'
    
    return app