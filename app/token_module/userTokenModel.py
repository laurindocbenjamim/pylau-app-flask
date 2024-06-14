from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from werkzeug.security import check_password_hash

from datetime import datetime, timedelta, timezone
from app import db
from ..configs.jwt_config import generate_token
#datetime.now(tz=timezone.utc)


class UserToken(db.Model):
    __tablename__ = 'user_token'
    token_id:Mapped[int] = db.Column(db.Integer, primary_key=True)
    #user_id:Mapped[int] = db.Column(db.Integer, db.ForeignKey('users.userID'))
    username:Mapped[str] = db.Column(db.String(100), nullable=False)
    token:Mapped[str] = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_exp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc) + timedelta(minutes=30))


    # This method is used to create a token
    def create_token(username):
        token = generate_token(username)
        try:
            obj = UserToken(username=username, token=token)
            db.session.add(obj)
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
    
    def to_dict(self):
        return {
            'token_id': self.token_id,
            'username': self.username,
            'token': self.token,
            'date_added': self.date_added,
            'date_exp': self.date_exp
        }
    
    # This method is used to update a token
    def update_token(user_id, username):
        token = generate_token(username)
        try:
            obj = UserToken.query.filter_by(username=username).first_or_404()
            #obj.user_id = user_id
            obj.username = username
            obj.token = token
            db.session.merge(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    # This method is used to update the date_exp of a token 
    def update_date_exp_token_by_user_id(user_id):
        try:
            #token = self.query.filter_by(user_id=user_id).first()
            #token.date_exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            #db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False

    # This method is used to get a token by the token 
    def get_token_by_token(token):
        try:
            token_obj = UserToken.query.filter_by(token=token).first_or_404()
            return True, token_obj
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    

    # This method is used to get a token by the username
    def get_token_by_user(username):
        try:
            token_obj = UserToken.query.filter_by(username=username).first_or_404()
            return True, token_obj
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
        
    def check_token_exists(token):
        try:
            token_obj = UserToken.query.filter_by(token=token).first()
            if token_obj:
                return True
            return False 
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    
    
    # This method is used to check if a token is expired
    def is_token_expired(self):
        return datetime.now(tz=timezone.utc) > self.date_exp

