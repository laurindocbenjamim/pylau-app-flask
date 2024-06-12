
from sqlalchemy.orm import Mapped,mapped_column, relationship

from app import db
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError

class TwoFAModel(db.Model):
    __tablename__ = 'two_fa_auth'
    two_fa_id:Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)
    userID:Mapped[int] = db.Column(db.Integer, nullable=False, unique=False)
    two_factor_auth_secret:Mapped[str] = db.Column(db.String(100), unique=False, nullable=False)  
    method_auth:Mapped[str] = db.Column(db.String(20),default="app", nullable=False) 
    is_active:Mapped[str] = db.Column(db.Boolean(), default=True, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.now())
    date_exp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc) + timedelta(days=30))
    
    def __repr__(self):
        return f'<TwoFAModel {self.two_fa_id} - {self.userID}>'
    
    def to_dict(self):
        return {
            'two_fa_id': self.two_fa_id,
            'userID': self.userID,
            'two_factor_auth_secret': self.two_factor_auth_secret,
            'method_auth': self.method_auth,
            'date_added': self.date_added
        }

    # create a User
    def save_two_fa_data(obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    