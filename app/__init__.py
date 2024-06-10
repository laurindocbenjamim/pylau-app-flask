


import os
import secrets
from flask import Flask, current_app, request, session, jsonify, render_template
from flask_cors import CORS
from flask_cors import cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from .db_conf import db, connect_to_db_server, init_db_server, migrate_db
from .app_conf import set_app_config

def create_application(type_db=None,test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    set_app_config(app)

    # Set the database URI
    connect_to_db_server(app,type_db)

     # Login Manager is needed for the the application 
    # to be able to log in and log out users

    login_manager = LoginManager()
    #login_manager.login_view = 'auth.user.login'
    login_manager.init_app(app)
    

    #from model.usermodel import db

    # Initialize the application extension
    db.init_app(app)
    
    # Create the database within the app context
    with app.app_context():
        db.create_all()


    from .routes import load_routes
    load_routes(app=app, db=db, login_manager=login_manager)
    
    # Migrate the db
    migrate_db(app)

    return app

