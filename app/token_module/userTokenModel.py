from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy import and_
from werkzeug.security import check_password_hash

from datetime import datetime, timedelta, timezone, date
from app.configs_package.modules.jwt_config import generate_token as generate_jwt_token, refresh_jwt_token, is_user_token_expired, force_jwt_token_expiration
from app.configs_package.modules.db_conf import db
from ..configs_package.modules.logger_config import get_message as set_logger_message
from flask import current_app

#datetime.now(tz=timezone.utc)


class UserToken(db.Model):
    __tablename__ = 'user_token'
    token_id:Mapped[int] = db.Column(db.Integer, primary_key=True)
    #user_id:Mapped[int] = db.Column(db.Integer, db.ForeignKey('users.userID'))
    username:Mapped[str] = db.Column(db.String(100), nullable=False)
    token:Mapped[str] = db.Column(db.String(255), unique=True, nullable=False)
    is_active:Mapped[str] = db.Column(db.Boolean(), default=False)
    datetime_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_added = db.Column(db.Date(), default=db.func.current_date())
    date_exp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc) + timedelta(minutes=30))


    # This method is used to create a token
    def create_token(username): 
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_now = datetime.strptime(date_now, '%Y-%m-%d %H:%M:%S')
        date_now_int = str(int(date_now.timestamp()))

        u_token = generate_jwt_token(username)
        
        try:
            obj = UserToken(username=username, token=u_token)
            db.session.add(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[create_token]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[create_token]: \n Exception: {str(e)}")
            return False, str(e)
    
    # This function refresh the user token throught the previous token
    def refresh_user_token(token): 
        return refresh_jwt_token(token)
    
    def is_user_token_expired(token):
        return is_user_token_expired(token)
       
    
    def to_dict(self):
        return {
            'token_id': self.token_id,
            'username': self.username,
            'token': self.token,
            'is_active': self.is_active,
            'date_added': self.date_added,
            'datetime_added': self.datetime_added,
            'date_exp': self.date_exp
        }
    
    # This method is used to update a token
    def update_token(user_id,last_token, new_token, username, is_active):
        try:
            obj = UserToken.query.filter(and_(UserToken.username==str(username), UserToken.token==str(last_token))).first_or_404()
            obj.token = str(new_token)
            obj.is_active = is_active
            obj.date_exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            #db.session.merge(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_token]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_token]: \n Exception: {str(e)}")
            return False, str(e)
    
    def refresh_user_token_____(user_id, username, is_active):
        token = generate_jwt_token(username)
        try:
            obj = UserToken.query.filter_by(username=str(username)).first_or_404()
            obj.token = token
            obj.is_active = is_active
            obj.date_exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            #db.session.merge(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    # This method is used to update the date_exp of a token 
    def expire_the_user_token_by_user(username, token):
        try:
            obj = UserToken.query.filter(and_(UserToken.username==str(username), UserToken.token==str(token))).first_or_404()
            obj.is_active = False
            obj.date_exp = datetime.now(tz=timezone.utc) - timedelta(minutes=5)
            
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    # This method forces the jwt user expiration token 
    def force_user_jwt_token_expiration(token):
        return force_jwt_token_expiration(token)
    
    # Delete a token by the token_id
    def delete_token_by_id(token_id):
        try:
            token = UserToken.query.filter_by(token_id=token_id).first_or_404()
            db.session.delete(token)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
        except Exception as e:
            db.session.rollback()
            return False
        
    # This method is used to get a token by the token 
    def get_token_by_token(token):
        try:
            token_obj = UserToken.query.filter_by(token=str(token)).first_or_404()
            return True, token_obj
        except SQLAlchemyError as e:
            set_logger_message(f"Error occured on METHOD[get_token_by_token]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            set_logger_message(f"Error occured on METHOD[get_token_by_token]: \n Exception: {str(e)}")
            return False, str(e)
    

    # This method is used to get a token by the username
    def get_token_by_user(username):
        try:
            token_obj = UserToken.query.filter_by(username=str(username)).first_or_404()
            return True, token_obj
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
        
    def check_token_exists(token):
        try:
            token_obj = UserToken.query.filter_by(token=str(token)).first()
            if token_obj:
                return True
            return False 
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    
    
    # This method is used to check if a token is expired
    def is_token_expired(self):
        return datetime.now(tz=timezone.utc).replace(tzinfo=None) > self.date_exp.replace(tzinfo=None)
    
    # Check if the token is already used
    def is_token_used(self):
        return self.is_used

