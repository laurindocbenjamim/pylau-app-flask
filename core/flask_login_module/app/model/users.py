from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from ..app import db
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from werkzeug.security import check_password_hash

from datetime import datetime

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)
    username: Mapped[str] = db.Column(db.String(100), unique=True)    
    email:Mapped[str] = db.Column(db.String(100), unique=True)
    password: Mapped[str] = db.Column(db.String(100))
    role:Mapped[str] = db.Column(db.String(100), default='user')
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __repr__(self):
        return '<User %r>' % self.username
    
    """ 
    This following property return True if the user is authenticated, i.e. 
    they have provided valid credentials. (Only authenticated users will fulfill the criteria of login_required.)
    """
    def is_authenticated(self):
        return True
    
    """
    This following property return True if this is an active user - in addition to being authenticated, they also 
    have activated their account, not been suspended, 
    or any condition your application has for rejecting an account. 
    Inactive accounts may not log in (without being forced of course).
    """
    def is_active(self):
        return True
    

    """
    This following property return True if this is an anonymous user. (Actual users should return False instead.)
    """
    def is_anonymous(self):
        return False
    
    """
    This method must return a str that uniquely identifies this user, and can be used to load the user from the user_loader callback. 
    Note that this must be a str - if the ID is natively an int or some other type, you will need to convert it to str.
    """
    def get_id(self):
        return self.id
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
        }
    
    def create_user(user_object):        
        try:
            db.session.add(user_object)
            db.session.commit()
            return 1
        except SQLAlchemyError as e:
            db.session.rollback()
            return str(e)
        except Exception as e:
            db.session.rollback()
            return str(e)

    def get_item_by_id(self,id):
        return next((item for item in self.list_users() if item['id'] == id), None)
    
    def check_password(self, password):
        # Implement password checking logic here
        # For example, you can compare the provided password with the stored password hash
        return check_password_hash(self.password,password)