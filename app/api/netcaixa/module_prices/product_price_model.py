
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
from ....configs_package.modules.logger_config import get_message as set_logger_message
from ....utils import _catch_sys_except_information

class ProductPriceModel(db.Model):
    """
    Product Price class: this class is  used to impplement the CRUD process for a 
    product object. It connects directly to our database  using the SQLAlchemy.

    On this class there  is following methods: Create(), Update(), Delete(), Select()
    """

    __tablename__ = "product_price"

    product_price_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    product_barcode: Mapped[str] = db.Column(
        db.String(100), nullable=False
    )
    product_description: Mapped[str] = db.Column(db.String(100), nullable=False)
    sale_price_01 = db.Column(db.Double(), nullable=False)
    sale_price_02 = db.Column(db.Double())
    sale_price_03 = db.Column(db.Double())
    pos_sale_price = db.Column(db.Double())
    price_date_added = db.Column(db.String(11), default=datetime.now().date())
    price_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    price_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    price_timestamp_added = db.Column(db.String(20), default=db.func.current_timestamp())
    price_update_added = db.Column(db.String(20))


    # Method to save the product price to the database
    def create(price: dict = dict)-> any:
        """
        This method is used to save a product price object
        into the database.

        Arguments:
            'price' -> is expected to be a dictionary with the product price fields

        Return:
            By default the function returns a boolean and the product price object if
            no error occured, if false return a boolean and an exception response
        """
        try:
            obj = ProductPriceModel(
                product_barcode = price['product_barcode'],
                product_description = price['product_description'],
                sale_price_01 = price['sale_price_01'],
                sale_price_02 = price['sale_price_02'],
                sale_price_03 = price['sale_price_03'],
                pos_sale_price = price['pos_sale_price'],
            )
            db.session.add(obj)
            db.session.commit()

            return True, obj
        
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PRODUCT PRICE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="CREATE PRODUCT PRICE")
            set_logger_message(error_info)
           
            return False, str(e)
        
    # Method to  update the  product price on database
    def update_product_info(price_id: str, price: dict = dict):
        """
        This method is used to update a product price object
        into the database.

        Arguments:
            'price_id' -> is the ID that indentify the object into the table. Is expected to be a String data type
            'price' -> is expected to be a dictionary with the product price fields

        Return:
            By default the function returns a boolean and the product price object if
            no error occured, if false return a boolean and an exception response
        """
        try:
            obj = ProductPriceModel.query.filter(and_(ProductPriceModel.product_price_id == price_id)).first_or_404()
            obj.product_barcode = price['product_barcode']
            obj.product_description = price['product_description']
            obj.price_update_added = datetime.now().strftime("%Y/%m/%d %H:%M:%S")           
            db.session.commit()

            return True, obj
        except sqlalchemy.exc as e:
            db.session.rollback()
            custom_message = "Product price ID not found."
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE PRODUCT PRICE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE PRODUCT PRICE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE PRODUCT PRICE")
            set_logger_message(error_info)
           
            return False, str(e)
        
        # Method to  update the  product price on database
    def update_prices(product_price_id: str, price: dict = dict):
        """
        This method is used to update a product price object
        into the database.

        Arguments:
            'product_price_id' -> is the ID that indentify the object into the table. Is expected to be a String data type
            'price' -> is expected to be a dictionary with the product price fields

        Return:
            By default the function returns a boolean and the product price object if
            no error occured, if false return a boolean and an exception response
        """
        try:
            obj = ProductPriceModel.query.filter(and_(ProductPriceModel.product_price_id == product_price_id)).first_or_404()
            obj.sale_price_01 = price['sale_price_01']
            obj.sale_price_02 = price['sale_price_02']
            obj.sale_price_03 = price['sale_price_03']
            obj.pos_sale_price = price['pos_sale_price']
            obj.price_update_added = datetime.now().strftime("%Y/%m/%d %H:%M:%S")   
            db.session.commit()

            return True, obj
        except NoResultFound as e:
            db.session.rollback()
            custom_message = "Product price not found."
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE PRODUCT PRICE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        except SQLAlchemyError as e:
            db.session.rollback()
            custom_message = "Database config error"
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE PRODUCT PRICE", custom_message=custom_message)
            set_logger_message(error_info)
            
            return False, custom_message
        
        except Exception as e:
            db.session.rollback()
            error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="UPDATE PRODUCT PRICE")
            set_logger_message(error_info)
           
            return False, str(e)

