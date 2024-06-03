
from sqlalchemy.orm import Mapped,mapped_column, relationship
from flask import jsonify
from core import db
from datetime import datetime

class TwoFAModel(db.Model):
    __tablename__ = 'two_fa_app_auth'
    two_fa_id:Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)
    userID:Mapped[int] = db.Column(db.Integer, nullable=False, unique=False)
    two_factor_auth_secret:Mapped[str] = db.Column(db.String(100), nullable=False)  
    type:Mapped[str] = db.Column(db.String(20),default="app", nullable=False) 
    date_added = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return f'<TwoFAModel {self.two_fa_id} - {self.userID}>'
    
    def to_dict(self):
        return {
            'two_fa_id': self.two_fa_id,
            'userID': self.userID,
            'two_factor_auth_secret': self.two_factor_auth_secret,
            'type': self.type,
            'date_added': self.date_added
        }
    