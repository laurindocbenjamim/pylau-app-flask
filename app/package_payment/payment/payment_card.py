
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

class PaymentCardModel(db.Model):
    """
    Payment class: this class is  used to impplement the CRUD process for a 
    payment object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "payment_card"
    # CREATE SEQUENCE card_id_seq START WITH 1 INCREMENT BY 1;
    # ALTER TABLE payment_card ALTER COLUMN card_id SET DEFAULT  nextval('card_id_seq');
    card_id: Mapped[int] = db.Column(
        db.Integer, Sequence('card_id_seq'), primary_key=True, autoincrement=True
    )
    student_id: Mapped[str] = db.Column(
        db.Integer, nullable=False
    )     
    card_number: Mapped[str] = db.Column(db.String(100), unique=True)
    card_name: Mapped[str] = db.Column(db.String(100))
    card_exp: Mapped[str] = db.Column(db.String(20))
    card_cvv: Mapped[str] = db.Column(db.String(10))
   
    card_date_added = db.Column(db.String(11), default=datetime.now().date())
    card_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    card_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    card_timestamp_added = db.Column(db.String(50), default=db.func.current_timestamp())
    card_update_added = db.Column(db.String(50))

    # Method to serialize the object
    def serialize(self):
        return {
            "card_id": self.card_id,
            "student_id": self.student_id,          
            "card_number": self.card_number,
            "card_name": self.card_name,
            "card_exp": self.card_exp,
            "card_cvv": self.card_cvv,
            "date_added": self.card_date_added,
            "card_year_added": self.card_year_added,
            "card_month_added": self.card_month_added,
            "card_timestamp_added": self.card_timestamp_added,
            "card_update_added": self.card_update_added,
        }
    
    # Method to save the card information to the database
    def create(student_id:int,card: dict = dict)-> any:
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
            obj = PaymentCardModel(
                student_id = student_id,
                card_number = card['card_number'],
                card_name = card['card_name'],
                card_exp = card['card_exp'],
                card_cvv = card['card_cvv'],
                date_added = card['date_added'],
                year_added = card['year_added'],
                month_added = card['month_added'],
                timestamp_added = card['timestamp_added'],
                update_added = card['update_added']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This payment card already exists"
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
    
    # Method to update the product payment card to the database
    def update(id:int,card: dict = dict)-> any:
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
            obj = PaymentCardModel.query.filter_by(card_id = id).first_or_404()

            obj.card_number = card['card_number']
            obj.card_name = card['card_name']
            obj.card_exp = card['card_exp']
            obj.card_cvv = card['card_cvv']
            obj.date_added = card['date_added']
            obj.year_added = card['year_added']
            obj.month_added = card['month_added']
            obj.timestamp_added = card['timestamp_added']
            obj.update_added = card['update_added']
            
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This payment card already exists"
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
    def update_card_info(id:int,card: dict = dict)-> any:
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

            #obj = PaymentModel.query.filter(and_(PaymentCardModel.card_id == id)).first_or_404()
            obj = PaymentCardModel.query.filter_by(card_id = id).first_or_404()

            obj.customer_card_number = card['customer_card_number'],
            obj.customer_card_name = card['customer_card_name'],
            obj.customer_card_exp = card['customer_card_exp'],
            obj.customer_card_cvv = card['customer_card_cvv'],
            obj.payment_update_added = card['payment_update_added']
            
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This payment code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT CARD", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT CARD", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PAYMENT CARD")
            set_logger_message(error_info)
           
            return False, str(e)