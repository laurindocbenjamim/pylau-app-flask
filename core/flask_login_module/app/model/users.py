from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from ..app import db

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(100), unique=True)
    password: Mapped[str] = db.Column(db.String(100))
    email:Mapped[str] = db.Column(db.String(100), unique=True)
    phone:Mapped[str] = db.Column(db.String(100), unique=True)
    role:Mapped[str] = db.Column(db.String(100), default='user')
    active = db.Column(db.Boolean(), default=False)
    two_factor = db.Column(db.Boolean(), default=False)
    two_factor_secret:Mapped[str] = db.Column(db.String(100))
    two_factor_recovery:Mapped[str] = db.Column(db.String(100))
    two_factor_recovery_codes:Mapped[str] = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime())
    #last_login = db.Column(db.DateTime())
    #last_login_ip = db.Column(db.String(100))
    #last_login_location = db.Column(db.String(100))
    #last_login_device = db.Column(db.String(100))
    #last_login_browser = db.Column(db.String(100))
    #last_login_os = db.Column(db.String(100))

    def __init__(self, username, password, email, phone, role, active, two_factor, two_factor_secret, two_factor_recovery, two_factor_recovery_codes, created_at, updated_at):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.role = role
        self.active = active
        self.two_factor = two_factor
        self.two_factor_secret = two_factor_secret
        self.two_factor_recovery = two_factor_recovery
        self.two_factor_recovery_codes = two_factor_recovery_codes
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'active': self.active,
            'two_factor': self.two_factor,
            'two_factor_secret': self.two_factor_secret,
            'two_factor_recovery': self.two_factor_recovery,
            'two_factor_recovery_codes': self.two_factor_recovery_codes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }