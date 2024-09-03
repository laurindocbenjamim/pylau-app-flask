
import traceback
import sys

import sqlalchemy.exc
from sqlalchemy.orm import Mapped
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound  # Import SQLAlchemyError
from sqlalchemy import and_
from werkzeug.security import check_password_hash


from datetime import datetime
from app.configs_package.modules.load_database import db
from app.configs_package.modules.logger_config import get_message as set_logger_message
from app.utils import _catch_sys_except_information

class PaymentModel(db.Model):
    """
    Payment class: this class is  used to impplement the CRUD process for a 
    payment object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "payments"

    payment_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    payment_code: Mapped[str] = db.Column(
        db.String(30), nullable=False, unique=True
    )
    payment_method: Mapped[str] = db.Column(
        db.String(50), nullable=False
    )
    customer_firstname: Mapped[str] = db.Column(db.String(100), nullable=False)
    customer_lastname: Mapped[str] = db.Column(db.String(100), nullable=False)    
    customer_payment_reference: Mapped[str] = db.Column(db.String(100))
    customer_card_number: Mapped[str] = db.Column(db.String(100))
    customer_card_name: Mapped[str] = db.Column(db.String(100))
    customer_card_exp: Mapped[str] = db.Column(db.String(10))
    customer_card_cvv: Mapped[str] = db.Column(db.String(10))
   
    payment_date_added = db.Column(db.String(11), default=datetime.now().date())
    payment_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    payment_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    payment_timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    payment_update_added = db.Column(db.String(20))


    # Method to save the product payment to the database
    def create(payment: dict = dict)-> any:
        """
        This method is used to save the payment object
        into the database.

        Arguments:
            'payment' -> is expected to be a dictionary with the payment fields

        Return:
            By default the function returns a boolean and the payment object if
            no error occured, if false return a boolean and an exception response
        """
        try:
            obj = PaymentModel(
                ppayment_code = payment['ppayment_code'],
                payment_description = payment['payment_description'],
                payment_details = payment['payment_details']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE")
            set_logger_message(error_info)
           
            return False, str(e)