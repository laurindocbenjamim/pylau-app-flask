
import traceback
import sys

import sqlalchemy.exc
from psycopg2 import errors as pg_errors
from sqlalchemy.orm import Mapped
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound  # Import SQLAlchemyError
from sqlalchemy import and_
from werkzeug.security import check_password_hash


from datetime import datetime
from app.configs_package.modules.load_database import db
from app.configs_package.modules.logger_config import get_message as set_logger_message
from app.utils import _catch_sys_except_information

class CourseContentModel(db.Model):
    """
    CourseContent class: this class is  used to impplement the CRUD process for a 
    course object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "courses_content"

    course_content_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    course_id: Mapped[str] = db.Column(
        db.String(100), nullable=False, unique=True
    )
    content_type: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    content_file: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    content_description: Mapped[str] = db.Column(db.String(100))
    content_thumbnail: Mapped[str] = db.Column(db.String(255))
    content_status: Mapped[bool] = db.Column(db.Boolean(), default=1)   
    content_date_added = db.Column(db.String(11), default=datetime.now().date())
    content_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    content_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    content_timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    content_update_added = db.Column(db.String(20))

    # Serialize the object
    def serialize(self):
        return {
            "course_content_id": self.course_content_id,
            "course_id": self.course_id,
            "content_type": self.content_type,
            "content_file": self.content_file,
            "content_description": self.content_description,
            "content_thumbnail": self.content_thumbnail,
            "content_status": self.content_status,           
            "content_date_added": self.content_date_added,
            "content_year_added": self.content_year_added,
            "content_month_added": self.content_month_added,
            "content_timestamp_added": self.content_timestamp_added,
            "content_update_added": self.content_update_added
        }

    # Method to save the product course to the database
    def create(course: dict = dict)-> any:
        """
        This method is used to save the course object
        into the database.

        Arguments:
            'CourseContentModel' -> is expected to be a dictionary with the CourseContentModel fields
        Return:
            By default the function returns a boolean and the course object if
            no error occured, if false return a boolean and an exception response
        """
        try:
            obj = CourseContentModel(
                course_id = course['course_id'],
                content_type = course['content_type'],
                content_file = ['content_file'],
                content_description = course['content_description'],
                content_thumbnail = course['content_thumbnail'],
                content_status = course['content_status'],           
                content_date_added = course['content_date_added'],
                content_year_added = course['content_year_added'],
                content_month_added = course['content_month_added'],
                content_timestamp_added = course['content_timestamp_added'],
                content_update_added = course['content_update_added']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        
        except pg_errors.UndefinedTable as e:
            db.session.rollback()
            custom_message = f"Undefined table error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE CONTENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This course code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE CONTENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE CONTENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE CONTENT")
            set_logger_message(error_info)
           
            return False, str(e)
        
    # Method to save the product course to the database
    def update(course: dict = dict)-> any:
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
            obj = CourseContentModel(
                course_id = course['course_id'],
                content_type = course['content_type'],
                content_file = ['content_file'],
                content_description = course['content_description'],
                content_thumbnail = course['content_thumbnail'],
                content_status = course['content_status'],           
                content_update_added = course['content_update_added']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE COURSE CONTENT", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE COURSE CONTENT")
            set_logger_message(error_info)
           
            return False, str(e)
    
    # Get all courses content
    def get():
        """
        This method  returns all courses content
        from database
        """
        try:
            obj = CourseContentModel.query.all()
            return obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get all courses content", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get all courses content", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
    
    # Geat all courses
    def get_content_by_course_id(course_id:int):
        """
        This method  returns all courses 
        from database
        """
        try:
            obj = CourseContentModel.query.filter_by(course_id=course_id).first_or_404()
            return True, obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_content_by_course_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except SQLAlchemyError as e:
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_content_by_course_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_content_by_course_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_content_by_course_id")
            set_logger_message(error_info)
           
            return False, str(e)
    