
import traceback
import sys

import sqlalchemy.exc
from sqlalchemy.orm import Mapped
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound  # Import SQLAlchemyError
from sqlalchemy import and_, Sequence
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

    # CREATE SEQUENCE payment_id_seq START WITH 1 INCREMENT BY 1;
    # ALTER TABLE payments ALTER COLUMN payment_id SET DEFAULT  nextval('payment_id_seq');
    payment_id: Mapped[int] = db.Column(
        db.Integer, Sequence('payment_id_seq'), primary_key=True, autoincrement=True
    )
    student_id: Mapped[str] = db.Column(
        db.Integer, nullable=False
    )
    payment_code: Mapped[str] = db.Column(
        db.String(30), nullable=False, unique=True
    )
    payment_method: Mapped[str] = db.Column(
        db.String(50), nullable=False
    )      
    payment_reference: Mapped[str] = db.Column(db.String(100))
    card_number: Mapped[str] = db.Column(db.String(100))   
    payment_date_added = db.Column(db.String(10), default=datetime.now().date())
    payment_year_added = db.Column(db.String(10), default=datetime.now().strftime("%Y"))
    payment_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    payment_timestamp_added = db.Column(db.String(50), default=db.func.current_timestamp())
    payment_update_added = db.Column(db.String(50))

    # Method to serialize the object
    def serialize(self):
        return {
            "payment_id": self.payment_id,
            "student_id": self.student_id,
            "payment_code": self.payment_code,
            "payment_method": self.payment_method,
            "payment_reference": self.payment_reference,
            "card_number": self.card_number,
            "payment_date_added": self.payment_date_added,
            "payment_year_added": self.payment_year_added,
            "payment_month_added": self.payment_month_added,
            "payment_timestamp_added": self.payment_timestamp_added,
            "payment_update_added": self.payment_update_added,
        }
    
    # Method to save the product payment to the database
    def create(student_id:int,payment: dict = dict)-> any:
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
                student_id = student_id,
                payment_code = payment['payment_code'],
                payment_method = payment['payment_method'],
                payment_reference = payment['payment_reference'],
                card_number = payment['card_number'],               
                payment_date_added = payment['payment_date_added'],
                payment_year_added = payment['payment_year_added'],
                payment_month_added = payment['payment_month_added'],
                payment_timestamp_added = payment['payment_timestamp_added'],
                payment_update_added = payment['payment_update_added']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "A payment with this code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
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
    
    # Method to update the product payment to the database
    def update(id:int,payment: dict = dict)-> any:
        """
        This method is used to update all the payment object
        into the database.

        Arguments:
            'payment' -> is expected to be a dictionary with the payment fields

        Return:
            By default the function returns a boolean and the payment object if
            no error occured, if false return a boolean and an exception response
        """
        try:

            #obj = PaymentModel.query.filter(and_(PaymentModel.payment == id)).first_or_404()
            obj = PaymentModel.query.filter_by(payment_id = id).first_or_404()

            obj.payment_code = payment['payment_code'],
            obj.payment_method = payment['payment_method'],
            obj.customer_payment_reference = payment['customer_payment_reference'],
            obj.customer_card_number = payment['customer_card_number'],            
            obj.payment_date_added = payment['payment_date_added'],
            obj.payment_year_added = payment['payment_year_added'],
            obj.payment_month_added = payment['payment_month_added'],
            obj.payment_timestamp_added = payment['payment_timestamp_added'],
            obj.payment_update_added = payment['payment_update_added']
            
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This payment code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT")
            set_logger_message(error_info)
           
            return False, str(e)
    
    # Method to update the product payment to the database
    def update_card_info(id:int,payment: dict = dict)-> any:
        """
        This method is used to update all the payment object
        into the database.

        Arguments:
            'payment' -> is expected to be a dictionary with the payment fields

        Return:
            By default the function returns a boolean and the payment object if
            no error occured, if false return a boolean and an exception response
        """
        try:

            #obj = PaymentModel.query.filter(and_(PaymentModel.payment == id)).first_or_404()
            obj = PaymentModel.query.filter_by(payment_id = id).first_or_404()

            obj.customer_card_number = payment['customer_card_number'],
            obj.payment_update_added = payment['payment_update_added']
            
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This payment code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT")
            set_logger_message(error_info)
           
            return False, str(e)