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


class Stock(db.Model):

    __tablename__ = "stock"

    stock_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    product_barcode: Mapped[str] = db.Column(
        db.String(100), nullable=False, unique=True
    )
    product_description: Mapped[str] = db.Column(db.String(100), nullable=False)
    product_unitary_price: Mapped[str] = db.Column(db.String(100))
    product_iva = db.Column(db.Double())
    product_iva_code: Mapped[str] = db.Column(db.String(10))
    product_profit = db.Column(db.Double())
    product_sale_price = db.Column(db.Double())    
    stock_pos: Mapped[str] = db.Column(db.String(100))
    stock_location: Mapped[str] = db.Column(db.String(100))
    stock_code: Mapped[str] = db.Column(db.String(50), default="0001")
    stock_date_added = db.Column(db.String(11), default=datetime.now().date())
    stock_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    stock_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    stock_datetime_added = db.Column(
        db.String(20), default=db.func.current_timestamp()
    )
    stock_date_updated = db.Column(db.String(20), nullable=True)

    