
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

class CourseProgressModel(db.Model):
    """
    Course class: this class is  used to impplement the CRUD process for a 
    course object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "course_progress"

    # CREATE SEQUENCE course_progress_id_seq START WITH 1 INCREMENT BY 1;
    # ALTER TABLE course_progress ALTER COLUMN course_progress_id SET DEFAULT nextval('course_progress_id_seq');
    course_progress_id: Mapped[int] = db.Column(
        db.Integer, Sequence('course_progress_id_seq'), primary_key=True, autoincrement=True
    )
    course_id: Mapped[int] = db.Column(
        db.String, nullable=False, unique=True
    )
    student_id: Mapped[int] = db.Column(
        db.Integer, nullable=False
    )
    total_lesson_completed: Mapped[int] = db.Column(
        db.Integer, default=0
    )
    last_lesson_completed: Mapped[str] = db.Column(db.String(200))   
    date_added = db.Column(db.String(11), default=datetime.now().date())
    year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    update_added = db.Column(db.String(20))

    # Serialize the object
    def serialize(self):
        return {
            "course_progress_id": self.course_progress_id,
            "course_id": self.course_id,
            "student_id": self.student_id,
            "total_lesson_completed": self.total_lesson_completed,
            "last_lesson_completed": self.last_lesson_completed,
            "date_added": self.date_added,
            "year_added": self.year_added,
            "month_added": self.month_added,
            "timestamp_added": self.timestamp_added,
            "update_added": self.update_added
        }

    # Method to save the product course to the database
    def create(column: dict = dict)-> any:
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
            obj = CourseProgressModel(
                course_id = column['course_id'],
                student_id = column['student_id'],
                total_lesson_completed = column['total_lesson_completed'],
                last_lesson_completed = column['last_lesson_completed'],
                date_added = column['date_added'],
                year_added = column['year_added'],
                month_added = column['month_added'],
                timestamp_added = column['timestamp_added']

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
    def update(course: dict = dict, course_progress_id:int = 0)-> any:
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
            obj = CourseProgressModel.query.filter_by(course_progress_id=course_progress_id).first_or_404()
            
            obj.total_lesson_completed = course['total_lesson_completed']
            obj.last_lesson_completed = course['last_lesson_completed']
            obj.update_added = course['timestamp_added']
            
            db.session.commit()

            return True, obj
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE COURSE PROGRESS", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE COURSE PROGRESS")
            set_logger_message(error_info)
           
            return False, str(e)
    
    # Geat all courses
    def get():
        """
        This method  returns all courses 
        from database
        """
        try:
            obj = CourseProgressModel.query.all()
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
    def get_by_course_progress_id(course_progress_id:int):
        """
        This method  returns all CourseProgressModel 
        from database
        """
        try:
            obj = CourseProgressModel.query.filter_by(course_progress_id=course_progress_id).first_or_404()
            return True, obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_course_progress_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except SQLAlchemyError as e:
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_course_progress_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_course_progress_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_course_progress_id")
            set_logger_message(error_info)
           
            return False, str(e)


    # Geat all courses
    def get_by_courseID_and_studentID(course_id:int = 0, student_id:int = 0):
        """
        This method  returns all CourseProgressModel 
        from database
        """
        try:
            obj = CourseProgressModel.query.filter(and_(CourseProgressModel.course_id==course_id, CourseProgressModel.student_id==student_id)).first_or_404()
            return True, obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_courseID_and_studentID", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except SQLAlchemyError as e:
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_courseID_and_studentID", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_courseID_and_studentID", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_courseID_and_studentID")
            set_logger_message(error_info)
           
            return False, str(e)
            
    def get_by_student_id(student_id:int):
        """
        This method  returns all CourseProgressModel 
        from database
        """
        try:
            obj = CourseProgressModel.query.filter_by(student_id=student_id).first_or_404()
            return True, obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_student_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except SQLAlchemyError as e:
            custom_message = f"Database config error {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_student_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_student_id", custom_message=custom_message)
            set_logger_message(error_info)
            
            return custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_student_id")
            set_logger_message(error_info)
           
            return False, str(e)
    