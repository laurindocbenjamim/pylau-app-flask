import traceback
import sys
import os
from flask import json
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # Import SQLAlchemyError
from sqlalchemy import and_
from werkzeug.security import check_password_hash


from datetime import datetime, timedelta, timezone
from app.configs_package.modules.load_database import db
from ....configs_package.modules.logger_config import get_message as set_logger_message
from ....utils import _catch_sys_except_information

from ..module_product.productModel import Product


class Stock(db.Model):

    __tablename__ = "stock"

    stock_id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_barcode: Mapped[str] = db.Column(
        db.String(100), nullable=False, unique=True
    )
    product_description: Mapped[str] = db.Column(db.String(100), nullable=False)
    product_unitary_price: Mapped[str] = db.Column(db.String(100))
    product_iva = db.Column(db.Double())
    product_iva_code: Mapped[str] = db.Column(db.String(10))
    product_profit = db.Column(db.Double())
    product_quantity = db.Column(db.Integer())
    stock_pos: Mapped[str] = db.Column(db.String(100))
    stock_location: Mapped[str] = db.Column(db.String(100))
    stock_code: Mapped[str] = db.Column(db.String(20), default="0001")
    stock_date_added = db.Column(db.String(11), default=datetime.now().date())
    stock_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    stock_month_added = db.Column(db.String(20), default=datetime.now().strftime("%m"))
    stock_datetime_added = db.Column(db.String(20), default=db.func.current_timestamp())
    stock_date_updated = db.Column(db.String(20), nullable=True)

    # Method to create stock
    def create(product=dict):
        try:
            obj = Stock(
                product_barcode=product["product_barcode"],
                product_description=product["product_description"],
                product_unitary_price=product["product_unitary_price"],
                product_iva=product["product_iva"],
                product_iva_code=product["product_iva_code"],
                product_profit=product["product_profit"],
                product_quantity=product["product_quantity"],
                stock_pos=product["stock_pos"],
                stock_location=product["stock_location"],
                stock_code=product["stock_code"],
                stock_date_added=product["stock_date_added"],
                stock_year_added=product["stock_year_added"],
                stock_month_added=product["stock_month_added"],
                stock_datetime_added=product["stock_datetime_added"],
                stock_date_updated=product["stock_date_updated"],
            )
            db.session.add(obj)
            db.session.commit()
            return True, obj
        
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This product already exist."
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK", custom_message=custom_message)
            set_logger_message(error_info)
           
            return False, custom_message
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    # Update method
    def update(product_barcode: str, product: dict) -> any:  # type: ignore
        """
        This method is used to update the product's fields

        Arguments
            product_id: this argument is required to filter the product object
            product: is dictionary of products
            and it will  update the product object according to the given fields

        Return:
            By default the function returns a boolean and the product object if
            none error occured, if false return a boolean and an exception response
        """
        try:
            obj = Stock.query.filter(
                and_(Stock.product_barcode == product_barcode)
            ).first()

            obj.product_barcode = product["product_barcode"]
            obj.product_description = product["product_description"]
            obj.product_unitary_price = product["product_unitary_price"]
            obj.product_iva = product["product_iva"]
            obj.product_iva_code = product["product_iva_code"]
            obj.product_profit = product["product_profit"]
            obj.product_quantity = product["product_quantity"]
            obj.stock_pos = product["stock_pos"]
            obj.stock_location = product["stock_location"]
            obj.stock_code = product["stock_code"]
            obj.stock_date_added = product["stock_date_added"]
            obj.stock_year_added = product["stock_year_added"]
            obj.stock_month_added = product["stock_month_added"]
            obj.stock_datetime_added = product["stock_datetime_added"]
            obj.stock_date_updated = product["stock_date_updated"]

            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[update_] \n \
                                       SQLAlchemyError: \n{str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    #
    # Delete method
    def delete_product(product_id: int) -> any:
        """
        This method is used t o delete  product object

        Arguments:
            The method receive as arguments the product ID
            which is used to remove  it from the database
        Return:
            By default the function returns a boolean and the product object if
            none error occured, if false return a boolean and an exception response
        """
        try:
            obj = Stock.query.filter_by(product_id=product_id).first_or_404()
            db.session.delete(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[delete_product] \n \
                                       SQLAlchemyError: \n{str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    # Get all product
    def get_all() -> bool and object:  # type: ignore
        """
        This method is used to filter all the products
        from the database.

        Return:
            It returns a boolean value and the product object
        """

        try:
            obj = Stock.query.all()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_all] \n \
                                       SQLAlchemyError:\n {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    def get_by_id(id):
        """
        This method is used to filter all the products
        from the database by ID

        Return:
            It returns a boolean value and the product object
        """

        try:
            obj = Stock.query.filter(and_(Stock.product_id == id)).first()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_by_id] \n \
                                       SQLAlchemyError: \n{str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    # Get Product by barcode
    def get_by_barcode(barcode):
        """
        This method is used to filter all the products
        from the database by Barcode

        Return:
            It returns a boolean value and the product object
        """

        try:
            obj = Stock.query.filter(
                and_(Stock.product_barcode == barcode)
            ).first_or_404()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_by_barcode] \n \
                                       SQLAlchemyError: \n{str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    def get_by_category(barcode):
        """
        This method is used to filter all the products
        from the database by Barcode

        Return:
            It returns a boolean value and the product object
        """

        try:
            obj = Stock.query.filter(
                and_(Stock.product_barcode == barcode)
            ).first_or_404()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_by_barcode] \n \
                                       SQLAlchemyError: \n{str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    def to_dict(item):
        return {
            "stock_id": item.stock_id,
            "product_barcode": item.product_barcode,
            "product_description": item.product_description,
            "product_unitary_price": item.product_unitary_price,
            "product_iva": item.product_iva,
            "product_iva_code": item.product_iva_code,
            "product_profit": item.product_profit,
            "product_quantity": item.product_quantity,
            "stock_pos": item.stock_pos,
            "stock_location": item.stock_location,
            "stock_code": item.stock_code,
            "stock_date_added": item.stock_date_added,
            "stock_year_added": item.stock_year_added,
            "stock_month_added": item.stock_month_added,
            "stock_datetime_added": item.stock_datetime_added,
            "stock_date_updated": item.stock_date_updated,
        }

    def serialize_objects(obj):
        objects = []
        for i, item in enumerate(obj):
            objects.append(
                {
                    "stock_id": item.stock_id,
                    "product_barcode": item.product_barcode,
                    "product_description": item.product_description,
                    "product_unitary_price": item.product_unitary_price,
                    "product_iva": item.product_iva,
                    "product_iva_code": item.product_iva_code,
                    "product_profit": item.product_profit,
                    "product_quantity": item.product_quantity,
                    "stock_pos": item.stock_pos,
                    "stock_location": item.stock_location,
                    "stock_code": item.stock_code,
                    "stock_date_added": item.stock_date_added,
                    "stock_year_added": item.stock_year_added,
                    "stock_month_added": item.stock_month_added,
                    "stock_datetime_added": item.stock_datetime_added,
                    "stock_date_updated": item.stock_date_updated,
                }
            )
        return objects
