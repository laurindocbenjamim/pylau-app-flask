
import os
from flask import Flask
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# This function is used to connect to the local database
def connect_to_server_db(app,type_db=None):
    if type_db == 'mysql':
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@localhost/testdb"
    elif type_db == 'postgres':
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/softcart"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdb.db"


def create_application(type_db=None,test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    app.config.from_mapping(
        SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Set the database URI
    connect_to_server_db(app,type_db)
    
    # Init the db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    """from . modules.codeskill import dictionaries
    app.register_blueprint(dictionaries.bpapp)

    from .modules.authmodule import authcontroller
    app.register_blueprint(authcontroller.bpapp)

    from . modules.authmodule import two_factor_auth
    app.register_blueprint(two_factor_auth.bpapp)
"""
    #from . modules.smtp import sendemail

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'rocketmc2009@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jgtkeopkbwoxkjoo'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    #sendemail.mail.init_app(app)
    #app.register_blueprint(sendemail.bpapp)

    from core.bpcomponents import get_bp_components
    get_bp_components(app, db)
    #from .modules.authmodule import two_factor_app_auth
    #app.register_blueprint(two_factor_app_auth.bpapp)

    # Import routes here
    #from core.routes import register_routes
    #register_routes(app, db)
    from core.routes import run_routes
    run_routes(app, db)

    # Imporst later

    Migrate(app, db)

    return app

