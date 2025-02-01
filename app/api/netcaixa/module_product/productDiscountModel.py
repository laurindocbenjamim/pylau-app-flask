import traceback
import sys
import os
from flask import json
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # Import SQLAlchemyError
from sqlalchemy import and_
from werkzeug.security import check_password_hash


from datetime import datetime, timedelta, timezone
from app.configs_package.modules.load_database import db
from ....configs_package.modules.logger_config import get_message as set_logger_message


class ProductDiscount(db.Model):

    __tablename__ = "products_discount"

    discount_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    product_barcode: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    discount_description: Mapped[str] = db.Column(db.String(100), nullable=False)
    discount_percent: Mapped[str] = db.Column(db.String(5))
    discount_value = db.Column(db.Double())    
    discount_status: Mapped[bool] = db.Column(db.Boolean(), default=False)
    discount_date_added = db.Column(db.String(11), default=datetime.now().date())
    discount_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    discount_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    discount_date_updated = db.Column(db.String(20), nullable=True)
