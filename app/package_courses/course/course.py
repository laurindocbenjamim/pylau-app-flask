
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

class CourseModel(db.Model):
    """
    Course class: this class is  used to impplement the CRUD process for a 
    course object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "courses"

    # CREATE SEQUENCE course_id_seq START WITH 1 INCREMENT BY 1;
    # ALTER TABLE courses ALTER COLUMN course_id SET DEFAULT nexval('course_id_seq')
    course_id: Mapped[int] = db.Column(
        db.Integer, Sequence('course_id_seq'), primary_key=True, autoincrement=True
    )
    course_code: Mapped[str] = db.Column(
        db.String(100), nullable=False, unique=True
    )
    course_description: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    course_level: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    course_details: Mapped[str] = db.Column(db.String(100))
    course_image: Mapped[str] = db.Column(db.String(255))
    course_view_url: Mapped[str] = db.Column(db.String(200))
    course_status: Mapped[bool] = db.Column(db.Boolean(), default=1)
    course_is_certified: Mapped[bool] = db.Column(db.Boolean(), default=0)
    course_total_lessons: Mapped[int] = db.Column(db.Integer)
    course_total_quizzes: Mapped[int] = db.Column(db.Integer)
    course_total_labs: Mapped[int] = db.Column(db.Integer)
    course_total_modules: Mapped[int] = db.Column(db.Integer)
    course_payment_link: Mapped[str] = db.Column(db.String(255))

    course_date_added = db.Column(db.String(11), default=datetime.now().date())
    course_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    course_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    course_timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    course_update_added = db.Column(db.String(20))

    # Serialize the object
    def serialize(self):
        return {
            "course_id": self.course_id,
            "course_code": self.course_code,
            "course_description": self.course_description,
            "course_details": self.course_details,
            "course_status": self.course_status,
            "course_is_certified": self.course_is_certified,
            "course_level": self.course_level,
            "course_image": self.course_image,
            "course_view_url": self.course_view_url,
            "course_total_lessons": self.course_total_lessons,
            "course_payment_link": self.course_payment_link,
            "course_total_quizzes": self.course_total_quizzes,
            "course_total_labs": self.course_total_labs,
            "course_total_modules": self.course_total_modules,
            "course_date_added": self.course_date_added,
            "course_year_added": self.course_year_added,
            "course_month_added": self.course_month_added,
            "course_timestamp_added": self.course_timestamp_added,
            "course_update_added": self.course_update_added
        }

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
                course_code = course['course_code'],
                course_description = course['course_description'],
                course_details = course['course_details'],
                course_status = course['course_status'],
                course_is_certified = course['course_is_certified'],
                course_view_url = course['course_view_url'],
                course_level = course['course_level'],
                course_image = course['course_image'],
                course_payment_link = course['course_payment_link'],
                course_total_lessons = course['course_total_lessons'],
                course_total_quizzes = course['course_total_quizzes'],
                course_total_labs = course['course_total_labs'],
                course_total_modules = course['course_total_modules']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        
        except pg_errors.UndefinedTable as e:
            db.session.rollback()
            custom_message = f"Undefined table error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This course code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE COURSE")
            set_logger_message(error_info)
           
            return False, str(e)
        
    # Method to save the product course to the database
    def update(course: dict = dict, course_id:int =0)-> any:
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
            obj = CourseModel.query.filter_by(course_id=course_id).first_or_404()

            obj.course_code = course['course_code']
            obj.course_description = course['course_description']
            obj.course_details = course['course_details']
            obj.course_status = course['course_status']
            obj.course_is_certified = course['course_is_certified']
            obj.course_view_url = course['course_view_url']
            obj.course_image = course['course_image']
            obj.course_payment_link = course['course_payment_link']
            obj.course_total_lessons = course['course_total_lessons']
            obj.course_total_quizzes = course['course_total_quizzes']
            obj.course_total_labs = course['course_total_labs']
            obj.course_total_modules = course['course_total_modules']
            
            db.session.commit()

            return True, obj
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE COURSE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE COURSE")
            set_logger_message(error_info)
           
            return False, str(e)
    
    # Geat all courses
    def get():
        """
        This method  returns all courses 
        from database
        """
        try:
            obj = CourseModel.query.all()
            return obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get all courses", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get all courses", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
    
    # Geat all courses
    def get_by_id(course_id:int):
        """
        This method  returns all courses 
        from database
        """
        try:
            obj = CourseModel.query.filter_by(course_id=course_id).first_or_404()
            return True, obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="check_if_enrolled", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except SQLAlchemyError as e:
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET COURSE by ID", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get courses by ID", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET COURSE by ID")
            set_logger_message(error_info)
           
            return False, str(e)
    