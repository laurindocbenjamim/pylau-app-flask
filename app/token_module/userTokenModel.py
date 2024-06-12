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
    def update_token(self, user_id, username):
        token = generate_token(username)
        try:
            #self.user_id = user_id
            self.username = username
            self.token = token
            db.session.commit()
            return self.token
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
        
    def update_date_exp_token_by_user_id(self, user_id):
        try:
            #token = self.query.filter_by(user_id=user_id).first()
            #token.date_exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            #db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
        
    def get_token_by_token(self, token):
        try:
            token_obj = self.query.filter_by(token=token).first()
            return {
                'token_id': token_obj.token_id,
                'username': token_obj.username,
                'token': token_obj.token,
                'date_added': token_obj.date_added,
                'date_exp': token_obj.date_exp
            }
        except SQLAlchemyError as e:
            return False

