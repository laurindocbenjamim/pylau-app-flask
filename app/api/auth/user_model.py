
import traceback
import sys
import os
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, Sequence
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import bleach


from datetime import datetime, timedelta, timezone
from app.configs_package.modules.load_database import db

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(256))
    social_id = db.Column(db.String(256))
    profile_image = db.Column(db.String(256))
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(256))
    email_confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Utility Functions
def sanitize_input(input_str):
    return bleach.clean(input_str, strip=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

"""# Routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')

@app.route('/reset-password')
def reset_password():
    return render_template('auth/reset.html')

@app.route('/profile')
@jwt_required()
def profile():
    return render_template('profile.html')"""
