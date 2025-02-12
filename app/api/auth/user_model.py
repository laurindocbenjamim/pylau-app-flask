import traceback
import sys
import os
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, Sequence
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import bleach


from datetime import datetime, timedelta, timezone
from app.configs_package.modules.logger_config import get_message as set_logger_message
from app.configs_package.modules.load_database import db


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    email_confirmed = db.Column(db.Boolean(), default=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    social_id = db.Column(db.String(256))
    profile_image = db.Column(db.String(256))
    has_2fa = db.Column(db.Integer(), nullable=True, default=1)
    is_active = db.Column(db.Integer(), nullable=True, default=1)    
    
    def __init__(self):
        # Create a default user
        #self.create_default_user()
        pass

    def create_default_user(self):

        try:
            db.session.add(
                User(
                    username="Admin",
                    email="feti@datatuning.com",
                    password_hash=generate_password_hash("Abel1234#"),
                    email_confirmed=True,
                    profile_image="https://img.icons8.com/?size=100&id=kDoeg22e5jUY&format=png&color=000000",
                )
            )
            db.session.commit()
            return True
        except IntegrityError as e:
            db.session.rollback()
            print("This user already exists")
            set_logger_message(
                f"This user already exists. Error occured on METHOD[create_default_user]: \n IntegrityError: {str(e)}"
            )
            return str(e)

        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(
                f"Error occured on METHOD[create_default_user]: \n SQLAlchemyError: {str(e)}"
            )
            return str(e)

        except Exception as e:
            db.session.rollback()
            set_logger_message(
                f"Error occured on METHOD[createcreate_default_user_user]: \n Exception: {str(e)}"
            )
            return str(e)

    #def set_password(self, password):
    #    self.password_hash = generate_password_hash(password)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def get_user_test(self):
        return {
            'id': 1,
            'username': 'Admin',
            'email': 'admin@datatuning.io',
            'password_hash': 'scrypt:32768:8:1$YxeSCCOd8MMe59Dp$e7e0937b77737ab7013d162fecb667285c5fa40d3050ac9657d46876afddc32afd5023ee10b2831bf48c2f20373e19ed5733e9beb2b556bd931cf45ec071517e'
        }

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    # Utility Functions
    def sanitize_input(input_str):
        return bleach.clean(input_str, strip=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )
