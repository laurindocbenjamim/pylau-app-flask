import traceback
import sys
import os
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy.exc import IntegrityError


from datetime import datetime, timedelta, timezone
from app.configs_package.modules.load_database import db
from ..configs_package.modules.logger_config import get_message as set_logger_message
#datetime.now(tz=timezone.utc)
from sqlalchemy import and_, Sequence

class HelpMessage(UserMixin, db.Model):

    __tablename__ = 'help_message'

    # CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;
    # ALTER TABLE users ALTER COLUMN user_id SET DEFAULT nextval('user_id_seq')

    h_message_id:Mapped[int] = db.Column(db.Integer, Sequence('h_message_id_seq'), primary_key=True, autoincrement=True)   
    name:Mapped[str] = db.Column(db.String(100), nullable=False)    
    email:Mapped[str] = db.Column(db.String(100), nullable=False)
    subject:Mapped[str] = db.Column(db.String(100), nullable=False)
    message:Mapped[str] = db.Column(db.String(300), nullable=False)
    phone:Mapped[str] = db.Column(db.String(20))    
    date_added:Mapped[str] = db.Column(db.String(20))
    datetime_added:Mapped[str] = db.Column(db.String(30))
    date_updated = db.Column(db.String(30), nullable=True)
    


    def __repr__(self):
        return '<HelpMessage %r>' % self.name
   
    
    def serialize(self):
        return {
            'h_message_id': self.h_message_id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,            
            'date_added': self.date_added,
            'datetime_added': self.datetime_added,
            'date_updated': self.date_updated
        }
    
    def create(self,obj):  
        
        status = False
        h_message_id = None   
        try:
            db.session.add(obj)
            db.session.commit()
            h_message_id = obj.h_message_id
            status = True
            return status,h_message_id
        
        except IntegrityError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[create_h_message]: \n SQLAlchemyError: {str(e)}")
            return status, str(e)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[create_h_message]: \n SQLAlchemyError: {str(e)}")
            return status, str(e)
        
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[create_h_message]: \n Exception: {str(e)}")
            return status, str(e)

    

    # This method delete user
    def delete(self,h_message_id):
        try:
            obj = HelpMessage.query.filter_by(h_message_id=h_message_id).first_or_404()
            db.session.delete(obj)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
        except Exception as e:
            db.session.rollback()
            return False

    # This method get all users
    def get_all(self):
        try:
            users = HelpMessage.query.all()
            return True, users
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)

    """
    This method selects the user by email.
    """
    def get_by_email(self,email):
        try:
            #user = Users.query.filter(and_(Users.email==str(email))).first()
            response = HelpMessage.query.filter_by(email=str(email)).first_or_404()
            return True, response
        except SQLAlchemyError as e:
            set_logger_message(f"Error occured on METHOD[get_HelpMessage_by_email]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            set_logger_message(f"Error occured on METHOD[get_HelpMessage_by_email]: \n Exception: {str(e)}")
            return False, str(e)
    
 