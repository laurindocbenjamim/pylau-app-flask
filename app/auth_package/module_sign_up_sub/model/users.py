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

class Users(UserMixin, db.Model):

    __tablename__ = 'users'

    userID:Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    username:Mapped[str] = db.Column(db.String(100), nullable=False, unique=True)
    firstname:Mapped[str] = db.Column(db.String(100), nullable=False)
    lastname:Mapped[str] = db.Column(db.String(100), nullable=False)
    email:Mapped[str] = db.Column(db.String(100), nullable=False)
    country:Mapped[str] = db.Column(db.String(20), nullable=False)
    country_code:Mapped[str] = db.Column(db.String(6), nullable=False)
    phone:Mapped[str] = db.Column(db.String(100), nullable=False)
    password:Mapped[str] = db.Column(db.String(255), nullable=False)
    role:Mapped[str] = db.Column(db.String(100), default='user')
    active:Mapped[bool] = db.Column(db.Boolean(), default=False)
    date_added = db.Column(db.Date(), default=db.func.current_date())
    datetime_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, nullable=True)
    


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
        if self.active == 1:
            return True
        return False
    

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
        return self.userID
    
    
    def to_dict(self):
        return {
            'userID': self.userID,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'country': self.country,
            'country_code': self.country_code,
            'phone': self.phone,
            'status': self.active,
            'role': self.role,
            'date_added': self.date_added,
            'date_updated': self.date_updated
        }
    
    def create_user(user_object):  
        status = False
        last_user_id = None   
        try:
            db.session.add(user_object)
            db.session.commit()
            last_user_id = user_object.userID
            status = True
            return status,last_user_id
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[create_user]: \n SQLAlchemyError: {str(e)}")
            return status, str(e)
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[create_user]: \n Exception: {str(e)}")
            return status, str(e)

    # This method update all user fields
    def update_user(user_id, user_object):
        status = False
        try:
            user = Users.query.filter_by(userID=user_id).first()
            user.firstname = user_object.firstname
            user.lastname = user_object.lastname
            user.email = user_object.email
            user.country = user_object.country
            user.country_code = user_object.country_code
            user.phone = user_object.phone
            user.role = user_object.role
            user.active = user_object.active
            user.date_updated = datetime.now()
            db.session.commit()
            return True, user_object
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_user]: \n Exception: {str(e)}")
            return status, str(e)
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_user]: \n Exception: {str(e)}")
            return status, str(e)
        
    # This method update user status
    def update_user_status(user_id, status):
        try:
            user = Users.query.filter_by(userID=user_id).first_or_404()
            user.active = status
            user.date_updated = datetime.now()
            db.session.commit()
            return True, user
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_user_status]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_user]: \n Exception: {str(e)}")
            return False, str(e)
    
    # This method update user role
    def update_user_role(user_id, role):
        try:
            user = Users.query.filter_by(userID=user_id).first_or_404()
            user.role = role
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_user_role]: \n SQLAlchemyError: {str(e)}")
            return False
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_user_role]: \n Exception: {str(e)}")
            return False
    
    # This method update user password
    def update_password(user_id, password):
        try:
            user = Users.query.filter_by(userID=user_id).first_or_404()
            user.password = password
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_password]: \n SQLAlchemyError: {str(e)}")
            return False
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_password]: \n Exception: {str(e)}")
            return False

    # This method delete user
    def delete_user(user_id):
        try:
            user = Users.query.filter_by(userID=user_id).first_or_404()
            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
        except Exception as e:
            db.session.rollback()
            return False

    # This method get all users
    def get_all_users():
        try:
            users = Users.query.all()
            return True, users
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)

    """
    This method selects the user by email.
    """
    def get_user_by_email(email):
        try:
            #user = Users.query.filter(and_(Users.email==str(email))).first()
            response = Users.query.filter_by(email=str(email)).first()
            return True, response
        except SQLAlchemyError as e:
            set_logger_message(f"Error occured on METHOD[get_user_by_email]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            set_logger_message(f"Error occured on METHOD[get_user_by_email]: \n Exception: {str(e)}")
            return False, str(e)
    
    """
    This method selects the user by ID.
    """
    def get_user_by_id(id):
        try:
            user = Users.query.filter_by(userID=id).first()
            return True, user
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)

    # This method selects the user by phone.
    def get_user_by_phone(phone):
        try:
            user = Users.query.filter_by(phone=phone).first_or_404()
            return True, user
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
        
    def check_email_exists(username):
        try:
            #user = Users.query.filter(and_(Users.email==str(username))).first()
            user = Users.query.filter_by(email=str(username)).first()
            if user:
                return True
            return False
        except SQLAlchemyError as e:
            set_logger_message(f"Error occured on METHOD[check_email_exists]: \n SQLAlchemyError: {str(e)}")
            return False
        except Exception as e:
            set_logger_message(f"Error occured on METHOD[check_email_exists]: \n Exception: {str(e)}")
            return False
    
    def check_phone_exists(phone_number):
        try:
            user = Users.query.filter_by(phone=str(phone_number)).first()
            if user:
                return True
            return False
        except SQLAlchemyError as e:
            set_logger_message(f"Error occured on METHOD[check_phone_exists]: \n SQLAlchemyError: {str(e)}")
            return False
        except Exception as e:
            set_logger_message(f"Error occured on METHOD[check_phone_exists]: \n Exception: {str(e)}")
            return False

    def get_item_by_id(self,id):
        return next((item for item in self.list_users() if item['id'] == id), None)
    
    def check_password(self, password):
        # Implement password checking logic here
        # For example, you can compare the provided password with the stored password hash
        return check_password_hash(self.password,password)

    
    get_limited_user_object = lambda data: Users(
        firstname=data.get('firstname'),
        lastname=data['lastname'],
        email=data['email'],
        country=data['country'],
        country_code=data['country_code'],
        phone=data['phone'],
        role=data['role'],
        active=data['active'],
        date_added=data['date_added'],
        date_updated=data['date_updated']
    )