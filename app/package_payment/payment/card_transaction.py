
import traceback
import sys

import sqlalchemy.exc
from psycopg2 import errors as pg_errors
from sqlalchemy.orm import Mapped
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound  # Import SQLAlchemyError
from sqlalchemy import and_, Sequence
from werkzeug.security import check_password_hash


from datetime import datetime
from app.configs_package.modules.load_database import db
from app.configs_package.modules.logger_config import get_message as set_logger_message
from app.utils import _catch_sys_except_information


class CardTransactionModel(db.Model):
    """
    Transaction class: this class is  used to impplement the CRUD process for a 
    payment object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "card_transactions"

    # CREATE SEQUENCE transaction_id_seq START WITH 1 INCREMENT BY 1;
    # ALTER TABLE card_transactions ALTER COLUMN transaction_id SET DEFAULT  nextval('transaction_id_seq');

    transaction_id: Mapped[int] = db.Column(
        db.Integer, Sequence('transaction_id_seq'), primary_key=True, autoincrement=True
    )
    student_id: Mapped[str] = db.Column(
        db.Integer, nullable=False
    )
    transaction_code: Mapped[str] = db.Column(
        db.String(30), nullable=False, unique=True
    )
    trans_from: Mapped[str] = db.Column(
        db.String(50), nullable=False
    )      
    trans_to: Mapped[str] = db.Column(db.String(100))   
    status: Mapped[str] = db.Column(db.Boolean())  
    date_added = db.Column(db.String(11), default=datetime.now().date())
    year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    timestamp_added = db.Column(db.String(50), default=db.func.current_timestamp())
    update_added = db.Column(db.String(50))

    # Method to serialize the object
    def serialize(self):
        return {
            "transaction_id":  self.transaction_id,
            "student_id":  self.student_id,
            "transaction_code":  self.transaction_code,
            "trans_from":  self.trans_from,
            "trans_to":  self.trans_to,
            "status":  self.status,
            "date_added":  self.date_added,
            "year_added":  self.year_added,
            "month_added":  self.month_added,
            "timestamp_added": self.timestamp_added,
            "update_added":  self.update_added,
        }
    
    
    # Method to save the product payment to the database
    def execute_transaction(**kwargs)-> any:
        """
        This method is used to save the payment transactions
        into the database.

        Arguments:
            'kwargs' -> is expected to be a list of objects to be saved into the database

        Return:
            By default the function returns a boolean
        """

        enroll_obj = kwargs.get('enroll_obj') 
        card_obj = kwargs.get('card_obj') 
        payment_obj = kwargs.get('payment_obj')
        #return [enroll_obj.serialize(), card_obj.serialize(), payment_obj.serialize()]
        try:
            """if kwargs.items():
                for key,obj in kwargs.items():
                    db.session.add(obj)
                    db.session.commit()"""
            db.session.add(enroll_obj)
            #db.session.commit()

            db.session.add(card_obj)
            #db.session.commit()

            db.session.add(payment_obj)
            db.session.commit()
            return True, "OK"
        except pg_errors.UndefinedTable as e:
            db.session.rollback()
            custom_message = str(e)
                        
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CARD TRANSACTIONS", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except IntegrityError as e:
            db.session.rollback()
            if 'course_id' in str(e):
                custom_message = f"Integrity violation. {str(e)}" #f"Student already enrolled at the course with ID {enroll_obj.course_id}."
            elif 'enroll_code' in str(e):
                custom_message = f"Integrity violation. Unique value required for the ENROLL CODE field. {str(e)}"
            elif 'card_number' in str(e):
                custom_message = f"Integrity violation. Unique value required for card number field. {str(e)}"
            elif 'payment_code' in str(e):
                custom_message = f"Integrity violation. Unique value required for the payment code field. {str(e)}"
            else:
                custom_message = f"Integrity violation. Unique value required. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CARD TRANSACTIONS", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"SQLAlchemyError error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CARD TRANSACTIONS", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CARD TRANSACTIONS", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        
        except Exception as e:
            db.session.rollback()
            custom_message = f"Exception error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CARD TRANSACTIONS", custom_message=custom_message)
            set_logger_message(error_info)
           
            return False, custom_message
    
   