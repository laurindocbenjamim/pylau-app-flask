
from sqlalchemy.orm import Mapped,mapped_column, relationship
from flask import jsonify
from core import db
from datetime import datetime

class Token(db.Model):
    __tablename__ = '_token'
    tokenID:Mapped[int] = db.Column(db.Integer, primary_key=True)
    userID:Mapped[int] = db.Column(db.Integer, nullable=False)
    token:Mapped[str] = db.Column(db.String(200), nullable=False)
    expire_time:Mapped[int] = db.Column(db.Integer, default=14, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    updated_date = db.Column(db.DateTime, nullable=True)
    #updated_date = db.Column(db.DateTime, default=datetime.now(datetime.UTC))

    def __repr__(self) -> str:
        return f"Token('{self.tokenID}', '{self.userID}', '{self.token}', '{self.expire_time}', '{self.created_date}', '{self.updated_date}')"
    
    def to_dict(self):
        return {
            'tokenID': self.tokenID,
            'userID': self.userID,
            'token': self.token,
            'expire_time': self.expire_time,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }