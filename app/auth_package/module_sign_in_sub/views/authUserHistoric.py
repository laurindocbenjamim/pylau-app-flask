import traceback
import sys
import os
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy import and_
from werkzeug.security import check_password_hash

from datetime import datetime, timedelta, timezone
from app.configs_package.modules.db_conf import db

from ....configs_package.modules.logger_config import get_message as set_logger_message
#datetime.now(tz=timezone.utc)


class AuthUserHistoric(db.Model):
    __tablename__ = 'auth_user_historic'
    auth_id:Mapped[int] = db.Column(db.Integer, primary_key=True)
    #user_id:Mapped[int] = db.Column(db.Integer, db.ForeignKey('users.userID'))
    user_id:Mapped[int] = db.Column(db.Integer, nullable=False)
    username:Mapped[str] = db.Column(db.String(100), nullable=False)
    device_id:Mapped[str] = db.Column(db.String(255), nullable=True)    
    is_logged_in:Mapped[bool] = db.Column(db.Boolean(), default=False)
    date_logged_in = db.Column(db.Date(), default=db.func.current_date())
    datetime_logged_in = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_logged_out = db.Column(db.DateTime, nullable=True)


    def create_auth_user(user_id, username, device_id):
        try:
            obj = AuthUserHistoric(user_id=user_id, username=username, device_id=device_id, is_logged_in=True)
            db.session.add(obj)
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
    
    
    def update_auth_user(user_id, username, status):
        try:
            obj = AuthUserHistoric.query.filter(and_(AuthUserHistoric.username==username, 
                                                     AuthUserHistoric.is_logged_in.is_(True),
                                                     AuthUserHistoric.date_logged_in==datetime.now().date()
                                                     )).first_or_404()
            obj.is_logged_in = status
            obj.date_logged_out = db.func.current_timestamp() #datetime.now(tz=timezone.utc)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            return False, str(e)
        
    def get_auth_user_by_username(username):
        try:
            obj = AuthUserHistoric.query.filter_by(username=username).first_or_404()
            return True, obj
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)

