
import os
import secrets
from flask import current_app as m_app
from flask_cors import CORS
from flask_cors import cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# This function is used to initialize the database
def init_db_server(app):

    # This function is used to migrate the database
    Migrate(app, db)
    
     # Init the db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    

    
    