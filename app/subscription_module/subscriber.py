import sys
import os
import traceback
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy import and_, Sequence
from werkzeug.security import check_password_hash

from datetime import datetime, timedelta, timezone, date
from app.configs_package.modules.jwt_config import generate_token as generate_jwt_token, refresh_jwt_token, is_user_token_expired, force_jwt_token_expiration
from app.configs_package.modules.load_database import db
from ..configs_package.modules.logger_config import get_message as set_logger_message


class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    # CREATE SEQUENCE subscriber_id_seq START WITH 1  INCREMENT BY 1;
    # ALTER TABLE subscribers ALTER COLUMN subscriber_id SET DEFAULT nextval('subscriber_id_seq');
    subscriber_id:Mapped[int] = db.Column(db.Integer, Sequence('subscriber_id_seq'), primary_key=True)    
    email:Mapped[str] = db.Column(db.String(100), nullable=False)
    is_active:Mapped[str] = db.Column(db.Boolean(), default=True)    
    year_added = db.Column(db.String(5), default=datetime.now().strftime('%Y'))
    month_added = db.Column(db.String(10), default=datetime.now().strftime('%m'))
    date_added = db.Column(db.Date(), default=datetime.now().date())
    datetime_added = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        return {
            'id': self.subscriber_id,
            'email': self.is_active,
            'year': self.year_added,
            'month': self.month_added,
            'date': self.date_added,
            'datetime': self.datetime_added
        }

    def save_subscriber(email)-> any:
        try:
            obj = db.session.add(Subscriber(email=email, is_active=True))
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[save_subscriber]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    # Check the email is already subscribed
    def check_subscriber(subscriber):
        try:
            obj = Subscriber.query.filter_by(email=subscriber).first()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[check_email]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            return False, str(e)
        except Exception as e:
            return False, str(e)