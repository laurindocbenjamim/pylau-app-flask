
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

class CourseModel(db.Model):
    """
    Course class: this class is  used to impplement the CRUD process for a 
    course object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "courses"

    course_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    course_code: Mapped[str] = db.Column(
        db.String(100), nullable=False, unique=True
    )
    course_description: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    course_details: Mapped[str] = db.Column(db.String(100), nullable=False)
   
    course_date_added = db.Column(db.String(11), default=datetime.now().date())
    course_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    course_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    course_timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    course_update_added = db.Column(db.String(20))


    # Method to save the product course to the database
    def create(course: dict = dict)-> any:
        """
        This method is used to save the course object
        into the database.

        Arguments:
            'course' -> is expected to be a dictionary with the course fields

        Return:
            By default the function returns a boolean and the course object if
            no error occured, if false return a boolean and an exception response
        """
        try:
            obj = CourseModel(
                pcourse_code = course['pcourse_code'],
                course_description = course['course_description'],
                course_details = course['course_details']
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