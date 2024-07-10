import os

from flask import Flask
from flask_cors import CORS


from app.configs_package.modules.load_database import db
from app.configs_package.modules.config import TestingConfig, DevelopmentConfig

def create_app(test_config=None):
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
        app.config.from_object(DevelopmentConfig())
    else:
        # Load the test config if passed in
        #app.config.from_mapping(test_config)
        app.config.from_object(TestingConfig())

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
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