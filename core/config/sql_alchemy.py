
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.ext.declarative import DeclaredBase
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

dbAlch = SQLAlchemy(model_class=Base)

def sqlite_db():
    # configure the SQLite database, relative to the app instance folder
    # SQLite, relative to Flask instance path
    current_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

def mysql_db():
    # MySQL / MariaDB
    current_app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://scott:tiger@localhost/project"
    

def postgres_db():
    # PostgreSQL
    current_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://scott:tiger@localhost/project"
    

# initialize the database by default to SQLite
def init_db(type_db=None):
    if type_db is None:
        sqlite_db()
    elif type_db == "mysql":
        mysql_db()
    elif type_db == "postgres":
        postgres_db()
    else:
        raise ValueError("Invalid database type")
    # initialize the database
    dbAlch.init_app(current_app)
    
    return dbAlch.create_all()