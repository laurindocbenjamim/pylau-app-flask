
import traceback
import sys

import sqlalchemy.exc
from psycopg2 import errors as pg_errors
from sqlalchemy.orm import Mapped
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound  # Import SQLAlchemyError
from sqlalchemy import and_, select, Sequence
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
    # CREATE SEQUENCE course_content_id_seq START WITH 1 INCREMENT BY 1;
    # ALTER TABLE courses_content ALTER COLUMN course_content_id SET DEFAULT nextval('course_content_id_seq');
    course_content_id: Mapped[int] = db.Column(
        db.Integer, Sequence('course_content_id_seq'), primary_key=True, autoincrement=True
    )
    course_id: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    content_type: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    content_module: Mapped[str] = db.Column(db.String(100))
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
            "content_module": self.content_module,
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

    def convert_to_list(obj):
        objects = []
        
        if not obj:
            return objects
        
        for i, item in enumerate(obj):
            objects.append(
                {   "course_content_id": int(item.course_content_id),
                    "course_id": int(item.course_id),
                    "content_module": int(item.content_module),
                    "content_type": item.content_type,
                    "content_file": item.content_file,
                    "content_description": item.content_description,
                    "content_thumbnail": item.content_thumbnail,
                    "content_status": item.content_status,           
                    "content_date_added": item.content_date_added,
                    "content_year_added": item.content_year_added,
                    "content_month_added": item.content_month_added,
                    "content_timestamp_added": item.content_timestamp_added,
                    "content_update_added": item.content_update_added
                }
            )
        return objects
    
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
                course_id = int(course['course_id']),
                content_type = str(course['content_type']).replace(' ', '').lower(),
                content_module = str(course['content_module']).replace(' ', ''),
                content_file = str(course['content_file']).replace(' ', ''),
                content_description = course['content_description'],
                content_thumbnail = course['content_thumbnail'],
                content_status = course['content_status'],           
                content_date_added = course['content_date_added'],
                content_year_added = course['content_year_added'],
                content_month_added = course['content_month_added'],
                content_timestamp_added = course['content_timestamp_added']
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
            custom_message = f"This course code already exists {str(e)}"
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
    def update(course: dict = dict, course_id:int=0)-> any:
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
            obj = CourseContentModel.query.filter(and_(CourseContentModel.course_id==course_id)).first_or_404()
            
            obj.content_type = str(course['content_type']).replace(' ', '').lower()
            obj.content_module = str(course['content_module']).replace(' ', '')
            obj.content_file = str(course['content_file']).replace(' ', '')
            obj.content_description = course['content_description']
            obj.content_thumbnail = course['content_thumbnail']
            obj.content_status = course['content_status']           
            obj.content_update_added = course['content_update_added']
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
            return False, obj
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get all courses content", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except pg_errors.DatabaseError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get all courses content", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
    
    # Geat all courses
    def get_content_by_course_id(course_id:int):
        """
        This method  returns all courses 
        from database

        Args:
            course_id
        Return:
            This method return two variables, True if no exception occure and a list of object with the course's content
        """
        try:
            #obj = CourseContentModel.query.filter_by(course_id=course_id).first_or_404()
            #query = select(CourseContentModel).where(CourseContentModel.course_id == course_id)
            #user_data = db.session.query(CourseContentModel).filter(CourseContentModel.course_id == course_id).all()
            obj = CourseContentModel.query.filter_by(course_id=course_id).all()
            
            #return True, db.session.execute(query).scalars().all()
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
            
            return False, custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_content_by_course_id")
            set_logger_message(error_info)
           
            return False, str(e)
    