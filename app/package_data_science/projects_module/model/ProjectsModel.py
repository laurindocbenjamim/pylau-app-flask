from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from werkzeug.security import check_password_hash

from datetime import datetime
from app import db

class Projects(UserMixin, db.Model):
    __tablename__ = 'projects'
    project_id: Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)
    username: Mapped[str] = db.Column(db.String(100), unique=True)    
    email:Mapped[str] = db.Column(db.String(100), unique=True)
    password: Mapped[str] = db.Column(db.String(100))
    role:Mapped[str] = db.Column(db.String(100), default='user')
    active:Mapped[bool] = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __repr__(self):
        return '<User %r>' % self.username
    
    