
from sqlalchemy.orm import Mapped,mapped_column, relationship
from flask import jsonify
from core import db
from datetime import datetime, timedelta, timezone

class AuthUser(db.Model):
    __tablename__ = 'auth_user'
    auth_user_id:Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)
    username:Mapped[str] = db.Column(db.String(100), nullable=False)    
    device:Mapped[str] = db.Column(db.String(100), nullable=True)
    device_ip:Mapped[str] = db.Column(db.String(100), nullable=True)
    device_mac:Mapped[str] = db.Column(db.String(100), nullable=True)
    #date_access = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_access = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f'<User accessed: {self.auth_user_id} - {self.username}>'
    
    def to_dict(self):
        return {
            'auth_user_id': self.auth_user_id,
            'username': self.username,
            'device': self.device,
            'date_access': self.date_access,
            'device_ip': self.device_ip,
            'device_mac': self.device_mac
        }
    
