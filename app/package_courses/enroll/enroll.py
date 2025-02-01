
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
    course_id: Mapped[int] = db.Column(
        db.Integer(), nullable=False
    )
    student_id: Mapped[str] = db.Column(
        db.Integer, nullable=False
    )
    student_firstname: Mapped[str] = db.Column(
        db.String(100), nullable=False
    ) 
    student_lastname: Mapped[str] = db.Column(
        db.String(100), nullable=False
    ) 
    
    student_address: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    student_address2: Mapped[str] = db.Column(
        db.String(100)
    )
    same_address: Mapped[str] = db.Column(db.String(100))
    save_info: Mapped[str] = db.Column(db.String(100))
    student_country: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    student_state: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    student_zip: Mapped[str] = db.Column(
        db.String(10), nullable=False
    ) 
    enroll_type: Mapped[str] = db.Column(
        db.String(50), default='7 Days'
    )   
    enroll_status: Mapped[str] = db.Column(db.Boolean(), default=True)
    enroll_obs: Mapped[str] = db.Column(db.String(100))
   
    enroll_date_added = db.Column(db.String(11), default=datetime.now().date())
    enroll_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    enroll_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    enroll_timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    enroll_update_added = db.Column(db.String(20))

    #  Method to serialize the object
    def serialize(self):
        return {
            "enroll_id": self.enroll_id, 
            "course_id": self.course_id,
            "student_id": self.student_id,
            "student_firstname": self.student_firstname,
            "student_lastname": self.student_lastname,
            "student_address": self.student_address,
            "student_address2": self.student_address2,
            "same_address": self.same_address,
            "student_country": self.student_country,
            "student_state": self.student_state,
            "student_zip": self.student_zip,
            "enroll_code": self.enroll_code,                
            "enroll_obs": self.enroll_obs,
            "enroll_status":  self.enroll_status,    
            "enroll_type": self.enroll_type,        
            "enroll_date_added":  self.enroll_date_added,
            "enroll_year_added":  self.enroll_year_added,
            "enroll_month_added":  self.enroll_month_added,
            "enroll_timestamp_added": self.enroll_timestamp_added,
            "enroll_update_added": self.enroll_update_added 
        }

    # Method to save the product enroll to the database
    def create(student_id:int, course_id: int,enroll: dict = dict)-> any:
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
                student_id = student_id,
                course_id = course_id,
                student_firstname = enroll['firstname'],
                student_lastname = enroll['lastname'],
                student_address = enroll['address'],
                student_address2 = enroll['address2'],
                student_country = enroll['country'],
                student_state = enroll['state'],
                same_address = enroll['same_address'],
                student_zip = enroll['student_zip'],
                enroll_code = enroll['enroll_code'],                
                enroll_obs = enroll['enroll_obs'],
                enroll_status = enroll['enroll_status'],    
                enroll_type = enroll['enroll_type'],           
                enroll_date_added = enroll['enroll_date_added'],
                enroll_year_added = enroll['enroll_year_added'],
                enroll_month_added = enroll['enroll_month_added'],
                enroll_timestamp_added = enroll['enroll_timestamp_added'],
                enroll_update_added = enroll['enroll_update_added']
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This enrollment code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL")
            set_logger_message(error_info)
           
            return False, str(e)
    

    # Method to update the product enroll to the database
    def update(id:int,enroll: dict = dict)-> any:
        """
        This method is used to update all the enroll object
        into the database.

        Arguments:
            'enroll' -> is expected to be a dictionary with the enroll fields

        Return:
            By default the function returns a boolean and the enroll object if
            no error occured, if false return a boolean and an exception response
        """
        try:

            #obj = EnrollModel.query.filter(and_(EnrollModel.enroll_id == id)).first_or_404()
            obj = EnrollModel.query.filter_by(enroll_id = id).first_or_404()
            
            obj.student_firstname = enroll['firstname']
            obj.student_lastname = enroll['lastname']
            obj.student_address = enroll['address']
            obj.student_address2 = enroll['address2']
            obj.same_address = enroll['same_address']
            obj.student_zip = enroll['student_zip']
            obj.enroll_code = enroll['enroll_code']                
            obj.enroll_obs = enroll['enroll_obs']
            obj.enroll_status = enroll['enroll_status']  
            obj.enroll_type = enroll['enroll_type'],          
            obj.enroll_date_added = enroll['enroll_date_added']
            obj.enroll_year_added = enroll['enroll_year_added']
            obj.enroll_month_added = enroll['enroll_month_added']
            obj.enroll_timestamp_added = enroll['enroll_timestamp_added']
            obj.enroll_update_added = enroll['enroll_update_added']
            
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This enrollment code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL")
            set_logger_message(error_info)
           
            return False, str(e)
        
     # Method to update the product enroll to the database
    def update_personal_info(id:int,enroll: dict = dict)-> any:
        """
        This method is used to update anly the personal information
        into the database.

        Arguments:
            'enroll' -> is expected to be a dictionary with the enroll fields

        Return:
            By default the function returns a boolean and the enroll object if
            no error occured, if false return a boolean and an exception response
        """
        try:

            obj = EnrollModel.query.filter_by(enroll_id = id).first_or_404()

            obj.student_firstname = enroll['firstname']
            obj.student_lastname = enroll['student_lastname']
            obj.student_address = enroll['address']
            obj.student_address2 = enroll['address2'] 
            obj.same_address = enroll['same_address']
            obj.student_zip = enroll['student_zip']           
            obj.enroll_update_added = enroll['enroll_update_added']
            
            db.session.commit()

            return True, obj
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL")
            set_logger_message(error_info)
           
            return False, str(e)


     # Method to update the product enroll to the database
    def update_enroll_info(id:int,enroll: dict = dict)-> any:
        """
        This method is used to update only the enrollement information
        into the database.

        Arguments:
            'enroll' -> is expected to be a dictionary with the enroll fields

        Return:
            By default the function returns a boolean and the enroll object if
            no error occured, if false return a boolean and an exception response
        """
        try:

            #obj = EnrollModel.query.filter(and_(EnrollModel.enroll_id == id)).first_or_404()
            obj = EnrollModel.query.filter_by(enroll_id = id).first_or_404()

            obj.enroll_code = enroll['enroll_code']                
            obj.enroll_obs = enroll['enroll_obs']
            obj.enroll_status = enroll['enroll_status']   
            obj.enroll_type = enroll['enroll_type'],         
            obj.enroll_date_added = enroll['enroll_date_added']
            obj.enroll_year_added = enroll['enroll_year_added']
            obj.enroll_month_added = enroll['enroll_month_added']
            obj.enroll_timestamp_added = enroll['enroll_timestamp_added']
            obj.enroll_update_added = enroll['enroll_update_added']
            
            db.session.commit()

            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This enrollment code already exists"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE ENROLL")
            set_logger_message(error_info)
           
            return False, str(e)

    # Method to get all the enroll to the database
    def get()-> any:
        """
        This method is used to get all the enroll object
        into the database.

        Return:
            return a list of dictionary
        """
        try:

            obj = EnrollModel.query.order_by(EnrollModel.course_description).all()
            return True, obj     
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET ALL ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message   
        except SQLAlchemyError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET ALL ENROLL", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET ALL ENROLL")
            set_logger_message(error_info)
           
            return False, str(e)  

    # Method to get all the enroll to the database
    def check_if_student_enrolled(student_id: str, course_id:int)-> any:
        """
        This method is used to get all the student enrollements
        into the database.

        Return:
            return a list of dictionary
        """
        try:

            #obj = EnrollModel.query.all()
            obj = EnrollModel.query.filter(and_(EnrollModel.student_id == student_id, EnrollModel.course_id == course_id)).first_or_404()
            return True, obj  
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="check_if_enrolled", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message       
        except SQLAlchemyError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="check_if_enrolled", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="check_if_enrolled")
            set_logger_message(error_info)
           
            return False, str(e)  


    # Method to get all the enroll to the database
    def get_by_student(student_id: int)-> any:
        """
        This method is used to get all the student enrollements
        into the database.

        Return:
            return a list of dictionary
        """
        try:

            obj = EnrollModel.query.filter_by(student_id=student_id).order_by(EnrollModel.course_id).all()
            return True, obj    
        except pg_errors.UndefinedTable as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="check_if_enrolled", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message     
        except SQLAlchemyError as e:
            custom_message = f"Database config error. {str(e)}"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_student", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="get_by_student")
            set_logger_message(error_info)
           
            return False, str(e)       