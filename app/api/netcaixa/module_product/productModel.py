
import traceback
import sys
import os
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from sqlalchemy import and_
from werkzeug.security import check_password_hash


from datetime import datetime, timedelta, timezone
from app.configs_package.modules.load_database import db
from ....configs_package.modules.logger_config import get_message as set_logger_message

class Product(db.Model):

    __tablename__ = 'products'

    product_id:Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    product_barcode:Mapped[str] = db.Column(db.String(100), nullable=False, unique=True)
    product_description:Mapped[str] = db.Column(db.String(100), nullable=False)
    product_category:Mapped[str] = db.Column(db.String(100))
    product_type:Mapped[str] = db.Column(db.String(100))    
    product_detail:Mapped[str] = db.Column(db.String(200))
    product_brand:Mapped[str] = db.Column(db.String(55))
    product_measure_unit:Mapped[str] = db.Column(db.String(10), default='unit')
    product_fixed_margin = db.Column(db.Double())
    product_status:Mapped[bool] = db.Column(db.Boolean(), default=False)
    product_retention_font:Mapped[str] = db.Column(db.String(50))
    product_date_added = db.Column(db.Date(), default=datetime.now().date())
    product_year_added = db.Column(db.String(4), default=datetime.now().strftime('%Y'))
    product_month_added = db.Column(db.String(20), default=datetime.now().strftime('%m'))
    product_datetime_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    product_date_updated = db.Column(db.DateTime, nullable=True)

    def _get_object(**kwargs):
        return Product(
            product_id = 1,  
            product_barcode = "003",
            product_description = "product3",
            product_category = "Vegetal",
            product_type = "Delicados" ,   
            product_detail ="product do campo",
            product_brand = "",
            product_measure_unit = "unit",
            product_fixed_margin = "10222",
            product_status = True,
            product_retention_font = ""
        )
    # Create method
    def create_product(product):
        """
        This method is used to save a product object
        into the database.

        Arguments: 
            'product' -> is expected to be a Product object

        Return: 
            By default the function returns a boolean and the product object if 
            none error occured, if false return a boolean and an exception response
        """
        try:
            db.session.add(product)
            db.session.commit()
            return True, product
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[createProduct]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")


    # Update method
    def update_product(product_id: int,**kwargs)-> any: # type: ignore
        """
        This method is used to update the product's fields

        Arguments
            product_id: this argument is required to filter the product object
            Kwargs: the method expects every fields of the product
            and it will  update the product object according to the given fields

        Return: 
            By default the function returns a boolean and the product object if 
            none error occured, if false return a boolean and an exception response
        """
        description = kwargs.get('description', None)
        barcode =  kwargs.get('barcode', None)
        try:
            obj = Product.query.filter(and_(Product.product_id == product_id)).first()

            obj.product_description = description if description is not None else obj.product_description
            obj.product_barcode = barcode if barcode is not None else obj.product_barcode

            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[update_product]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")
    
    # Delete method
    def delete_product(product_id: int) -> any:
        """
        This method is used t o delate  product object 

        Arguments:
            The method receive as arguments the product ID 
            which is used to remove  it from the database
        Return: 
            By default the function returns a boolean and the product object if 
            none error occured, if false return a boolean and an exception response
        """
        try:
            pass
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[delete_product]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")
    


    # Get all product
    def get_all_products()-> bool and object: # type: ignore
        """
            This method is used to filter all the products
            from the database.

            Return:
                It returns a boolean value and the product object
        """

        try:
            obj = Product.query.all().sort('ASC')
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[delete_product]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")

    def get_by_id(id):
        return []
    # Get all method test
    def get_all_():
        return [
            {
                'product_id': 1,  
                'product_barcode': "001",
                'product_description': "product1",
                'product_category': "Vegetal",
                'product_type': "Delicados" ,   
                'product_detail':"product do campo",
                'product_brand': "",
                'product_measure_unit': "unit",
                'product_fixed_margin': "10",
                'product_status': True,
                'product_retention_font': "",
                'product_date_added': "2024/09/09",
                'product_year_added': "2024",
                'product_month_added': "09",
                'product_datetime_added': "2024/09/09 23:03",
                'product_date_updated': "",
            },
            {
                'product_id': 2,  
                'product_barcode': "002",
                'product_description': "product2",
                'product_category': "Vegetal",
                'product_type': "Delicados" ,   
                'product_detail':"product do campo",
                'product_brand': "",
                'product_measure_unit': "unit",
                'product_fixed_margin': "10",
                'product_status': True,
                'product_retention_font': "",
                'product_date_added': "2024/09/09",
                'product_year_added': "2024",
                'product_month_added': "09",
                'product_datetime_added': "2024/09/09 23:03",
                'product_date_updated': "",
            },
        ]

