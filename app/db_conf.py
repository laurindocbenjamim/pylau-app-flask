
import os
import secrets
from flask import current_app as m_app
from flask_cors import CORS
from flask_cors import cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# This function is used to connect to the local database
def connect_to_db_server(app,type_db=None):
    if type_db == 'mysql':
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@localhost/testdb"
    elif type_db == 'postgres':
        local_db = "postgresql://postgres:root@localhost:5432/test"
        cloud_db = "postgres://fiysuzvofhprpp:ab6e8ad51efac658eca5c1b66056b9438d8866a522daeb3fee983b66970c0883@ec2-52-31-2-97.eu-west-1.compute.amazonaws.com:5432/db5veivij96r5u?sslmode=require"
        app.config["SQLALCHEMY_DATABASE_URI"] = cloud_db
        
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test3.db"

    """
    The line of code you provided is used to configure the behavior of SQLAlchemy, which is a popular Object-Relational Mapping (ORM) library for Python. 

In particular, [`app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FUtilizador%2FOneDrive%2FDocumentos%2FPythonProject%2FFlask-Projects%2Fpylau-app-flask%2Fapplication%2Fdb_conf.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A13%2C%22character%22%3A25%7D%5D "application/db_conf.py") is used to disable the SQLAlchemy's modification tracking feature. 

By default, SQLAlchemy tracks modifications made to objects and emits signals to inform the application about these changes. However, this feature can be resource-intensive and may not be necessary for all applications. 

Setting `SQLALCHEMY_TRACK_MODIFICATIONS` to `False` disables this tracking feature, which can improve performance in certain scenarios where modification tracking is not needed.
    """
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False




# This function is used to initialize the database
def init_db_server(app):
     # Init the db
    db.init_app(app)

    with app.app_context():
        db.create_all()

# This function is used to migrate the database
def migrate_db(app):
    Migrate(app, db)