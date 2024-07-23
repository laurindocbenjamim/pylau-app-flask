


import os
import secrets
from flask import Flask, current_app, request, session, jsonify, render_template
from flask_cors import CORS

from flask_migrate import Migrate
from flask_login import LoginManager
from .configs_package import DevelopmentConfig, TestingConfig, ProductionConfig

from .configs_package.modules.load_database import db
from .configs_package.modules.load_database import init_db_server

#def create_application(**kwargs):
    #type_db = kwargs.get('type_db', None)
    #test_config = kwargs.get('test_config', None),
    
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
        app.config.from_object(TestingConfig())

    
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
    #migrate_db(app)

    @app.route('/hello')
    def hello():
        resp = db.session.execute('SELECT 1+5')
        
        return f'Hello, World {resp}'

    return app




"""

"""
def create_app(JDBC="sqlite",test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    """
    app.config.from_mapping(
        SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI="sqlite:///flaskr.sqlite",
    )
    """

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

    """
    
    # import and call the database configuration
    #from . import db
    #from . config import db

    db.init_app(app)

    # Create the database within the app context
    with app.app_context():
        db.create_all()

    Migrate(app, db)

    """
    # import and call the database configuration
    from app.configs_package.modules.load_database import init_db_server  
    init_db_server(app)

    #from .routes import load_routes
    #from .configs_package.views.routes import load_routes
    from .utils.views.routes import load_routes
    load_routes(app=app, db=db, login_manager=login_manager)
    
    # Simple page that say hello
    @app.route("/new-post")
    def new_post():
        return {
            'post': "Hello world!"
        }

    # Simple page that say hello
    @app.route("/hello")
    def hello():
        return 'Hello, World'
    
    return app