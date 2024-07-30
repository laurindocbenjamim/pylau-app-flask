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


class ProductHasPrice(db.Model):

    __tablename__ = "product_has_price"

    price_id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_barcode: Mapped[str] = db.Column(db.String(100), nullable=False)
    unitary_price = db.Column(db.Double())
    sale_price_1 = db.Column(db.Double())
    sale_price_2 = db.Column(db.Double())
    sale_price_with_iva = db.Column(db.Double())
    sale_pos_price = db.Column(db.Double())
    price_date_added = db.Column(db.String(11), default=datetime.now().date())
    price_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    price_month_added = db.Column(db.String(20), default=datetime.now().strftime("%m"))
    price_datetime_added = db.Column(db.String(20), default=db.func.current_timestamp())
    price_date_updated = db.Column(db.String(20), nullable=True)

    # Method to create price
    def create(product=dict):
        try:
            obj = ProductHasPrice(
                product_barcode=product["product_barcode"],
                unitary_price = product["unitary_price"],
                sale_price_1 = product["sale_price_1"],
                sale_price_2 = product["sale_price_2"],
                sale_price_with_iva = product["sale_price_with_iva"],
                sale_pos_price = product["sale_pos_price"],
                price_date_added=product["price_date_added"],
                price_year_added=product["price_year_added"],
                price_month_added=product["price_month_added"],
                price_datetime_added=product["price_datetime_added"],
                price_date_updated=product["price_date_updated"],
            )
            db.session.add(obj)
            db.session.commit()
            return True, obj
        
        
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This price already exist."
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
            obj = ProductHasPrice.query.filter(
                and_(ProductHasPrice.product_barcode == product_barcode)
            ).first_or_404(description=f"Failed to update. No product with the barcode [{product}] has been found.")

            
            obj.product_barcode=product["product_barcode"]
            obj.unitary_price = product["unitary_price"]
            obj.sale_price_1 = product["sale_price_1"]
            obj.sale_price_2 = product["sale_price_2"]
            obj.sale_price_with_iva = product["sale_price_with_iva"]
            obj.sale_pos_price = product["sale_pos_price"]
            obj.price_date_added=product["price_date_added"]
            obj.price_year_added=product["price_year_added"]
            obj.price_month_added=product["price_month_added"]
            obj.price_datetime_added=product["price_datetime_added"]
            obj.price_date_updated=product["price_date_updated"]            

            db.session.commit()
            return True, obj
        except IntegrityError as e:
            db.session.rollback()
            custom_message = "This product already exist."
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE STOCK", custom_message=custom_message)
            set_logger_message(error_info)
           
            return False, custom_message
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE STOCK", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE STOCK")
            set_logger_message(error_info)
           
            return False, str(e)

    #
    # Delete method
    def delete_product(product: int | str) -> any:
        """
        This method is used t o delete  product object

        Arguments:
            The method receive as arguments a product item
            which is used to remove  it from the database
        Return:
            By default the function returns a boolean and the product object if
            none error occured, if false return a boolean and an exception response
        """
        try:
            obj = ProductHasPrice.query.filter_by(product_barcode=product)\
            .first_or_404(description=f"Failed to delete. No product with the barcode [{product}] has been found.")
            db.session.delete(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="DELETE STOCK", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="DELETE STOCK")
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
            obj = ProductHasPrice.query.all()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET ALL STOCK", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET ALL STOCK")
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
            obj = ProductHasPrice.query.filter(and_(ProductHasPrice.stock_id == id))\
            .first_or_404(description=f"No product with the ID [{id}] has been found.")
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET_BY_ID", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET_BY_ID")
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
            obj = ProductHasPrice.query.filter(
                and_(ProductHasPrice.product_barcode == barcode)
            ).first_or_404(description=f"No product with the barcode [{barcode}] has been found.")
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET_BY_BARCODE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET_BY_BARCODE")
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
            obj = ProductHasPrice.query.filter(
                and_(ProductHasPrice.product_barcode == barcode)
            ).first_or_404(description=f"No product with the barcode [{barcode}] has been found.")
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET_BY_CATEGORY", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="GET_BY_CATEGORY")
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
