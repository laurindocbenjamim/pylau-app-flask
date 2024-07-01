
import traceback
import sys
import os
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy import and_, text
from ..configs_package.modules.logger_config import get_message as set_logger_message
from ..configs_package import db

def execute_sql(SQL):
    
    try:
        #resp = db.session.execute(db.select(table).order_by(User.firstname)).scalars()
        resp = db.session.execute(text(SQL))
        #rows = resp.fetchall()
        db.session.commit()
        return True, resp
    except SQLAlchemyError as e:
        db.session.rollback()
        set_logger_message(f"Error occured on METHOD[execute_sql]: \n SQLAlchemyError: {str(e)}")
        return False, str(e)
    except Exception as e:
        db.session.rollback()
        set_logger_message(f"Error occured on METHOD[execute_sql]: \n Exception: {str(e)}")
        return False, str(e) 

