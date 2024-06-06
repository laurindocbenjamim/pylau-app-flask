
from sqlalchemy.orm import Mapped,mapped_column, relationship
from core import db
from datetime import datetime, timedelta, timezone

# default=datetime.now(tz=timezone.utc)
class User(db.Model):
    __tablename__ = 'users'
    userID:Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)   
    firstname:Mapped[str] = db.Column(db.String(100), nullable=False)
    lastname:Mapped[str] = db.Column(db.String(100), nullable=False)
    email:Mapped[str] = db.Column(db.String(100), nullable=False)
    country:Mapped[str] = db.Column(db.String(20), nullable=False)
    country_code:Mapped[str] = db.Column(db.String(6), nullable=False)
    phone:Mapped[str] = db.Column(db.String(100), nullable=False)
    password:Mapped[str] = db.Column(db.String(255), nullable=False)
    two_factor_auth_secret:Mapped[str] = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(10), default='inactive', nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    date_updated = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.userID} - {self.email}>'
    
    def to_dict(self):
        return {
            'userID': self.userID,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'password': self.password,
            'email': self.email,
            'country': self.country,
            'country_code': self.country_code,
            'phone': self.phone,
            'status': self.status,
            'two_factor_auth_secret': self.two_factor_auth_secret,
            'date_added': self.date_added,
            'date_updated': self.date_updated
        }
    
    def to_limited_dict(self):
        return {
            'userID': self.userID,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'country': self.country,
            'country_code': self.country_code,
            'phone': self.phone,
            'status': self.status,
            'date_added': self.date_added,
            'date_updated': self.date_updated
        }
    
