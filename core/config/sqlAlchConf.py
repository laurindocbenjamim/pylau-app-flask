

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)


def sqlite_db():
    # configure the SQLite database, relative to the app instance folder
    # SQLite, relative to Flask instance path
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqliteproject.db"

def mysql_db():
    # MySQL / MariaDB
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://scott:tiger@localhost/project"
    
def postgres_db():
    # PostgreSQL
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://scott:tiger@localhost/project"
    
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
    
    # initialize the app with the extension
    db.init_app(app)
    return db


# initialize the database
mDB = init_db()

# create the database Model

from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import Mapped,mapped_column, relationship
from datetime import datetime

class User(db.Model):
    id: Mapped[int] = Column(db.Integer,primary_key=True)
    firstname: Mapped[str] = Column(db.String(120), nullable=False)
    lastname: Mapped[str] = Column(db.String(120), nullable=False)
    email: Mapped[str] = Column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = Column(db.String(255), nullable=False)
    country: Mapped[str] = Column(db.String(120), nullable=False)
    countrycode: Mapped[str] = Column(db.String(6), nullable=False)
    phone: Mapped[int] = Column(db.Integer, unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Create a string representation of the model
    def __repr__(self) -> str:
        return '<Name %r>' % self.email
    

def createContext():
    with app.app_context():
        db.create_all()

createContext()

# Query the database
# Select all users

def selectAllUsers():
    users = db.session.execute(db.select(User).order_by(User.firstname)).scalars()
    if users is not None:
        for user in users:
            print(user.firstname)
    return users


# Create a new user
def createUser():
    user = User(firstname="John", lastname="Doe", email="email@email.com", password="123456", country="USA", countrycode="+1", phone=1234567890)
    db.session.add(user)
    db.session.commit()
    print("User created")
    return user.id


createUser()
selectAllUsers()
