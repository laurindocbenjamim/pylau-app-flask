
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

class EnrollModel(db.Model):
    """
    Enroll class: this class is  used to impplement the CRUD process for a 
    enroll object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "enrolls"

    enroll_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    enroll_code: Mapped[str] = db.Column(
        db.String(40), nullable=False, unique=True
    )
    student_id: Mapped[str] = db.Column(
        db.String(30), nullable=False
    )
    student_name: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    course_code: Mapped[str] = db.Column(
        db.String(40), nullable=False
    )
    course_description: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    enroll_status: Mapped[str] = db.Column(db.Boolean(), default=True)
    enroll_obs: Mapped[str] = db.Column(db.String(100), nullable=False)
   
    enroll_date_added = db.Column(db.String(11), default=datetime.now().date())
    enroll_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    enroll_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    enroll_timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    enroll_update_added = db.Column(db.String(20))


    # Method to save the product enroll to the database
    def create(enroll: dict = dict)-> any:
        """
        This method is used to save the enroll object
        into the database.

        Arguments:
            'enroll' -> is expected to be a dictionary with the enroll fields

        Return:
            By default the function returns a boolean and the enroll object if
            no error occured, if false return a boolean and an exception response
        """
        try:
            obj = EnrollModel(
                penroll_code = enroll['enroll_code'],
                enroll_description = enroll['enroll_description'],
                enroll_details = enroll['enroll_details']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL")
            set_logger_message(error_info)
           
            return False, str(e)