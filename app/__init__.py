


import os
import secrets
from flask import Flask, current_app, request, session, jsonify, render_template
from flask_cors import CORS
from flask_cors import cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .configs_package import DevelopmentConfig, TestingConfig, ProductionConfig

from .configs_package.modules.db_conf import db
from .configs_package.modules.db_conf import connect_to_db_server, migrate_db
from .configs_package.modules.app_conf import set_app_config


def create_application(type_db=None,test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    # Load the application configurations from an object file

    if test_config is None:
        # load the instance config, if it exists, when not testing
        #app.config.from_pyfile('config.py', silent=True)
        app.config.from_object(DevelopmentConfig(type_db))
    else:
        # load the test config if passed in
        #app.config.from_mapping(test_config)
        app.config.from_object(TestingConfig)

    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # This configuration uses from_mapping
    #set_app_config(app)

    # Set the database URI
    #connect_to_db_server(app,type_db)

     # Login Manager is needed for the the application 
    # to be able to log in and log out users

    login_manager = LoginManager()
    login_manager.init_app(app)
    #login_manager.login_view = 'auth.user.login'
    

    #from model.usermodel import db

    # Initialize the application extension
    db.init_app(app)
    
    # Create the database within the app context
    with app.app_context():
        db.create_all()


    #from .routes import load_routes
    #from .configs_package.views.routes import load_routes
    from .utils.views.routes import load_routes
    load_routes(app=app, db=db, login_manager=login_manager)
    
    # Migrate the db
    migrate_db(app)

    return app

