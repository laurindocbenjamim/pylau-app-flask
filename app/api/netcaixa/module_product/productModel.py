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


class Product(db.Model):

    __tablename__ = "products"

    product_id: Mapped[int] = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    product_barcode: Mapped[str] = db.Column(
        db.String(100), nullable=False, unique=True
    )
    product_description: Mapped[str] = db.Column(db.String(100), nullable=False)
    product_category: Mapped[str] = db.Column(db.String(100))
    product_type: Mapped[str] = db.Column(db.String(100))
    product_detail: Mapped[str] = db.Column(db.String(200))
    product_brand: Mapped[str] = db.Column(db.String(55))
    product_measure_unit: Mapped[str] = db.Column(db.String(10), default="unit")
    product_fixed_margin = db.Column(db.Double())
    product_status: Mapped[bool] = db.Column(db.Boolean(), default=False)
    product_retention_font: Mapped[str] = db.Column(db.String(50))
    product_date_added = db.Column(db.String(11), default=datetime.now().date())
    product_year_added = db.Column(db.String(4), default=datetime.now().strftime("%Y"))
    product_month_added = db.Column(
        db.String(20), default=datetime.now().strftime("%m")
    )
    product_datetime_added = db.Column(
        db.String(20), default=db.func.current_timestamp()
    )
    product_date_updated = db.Column(db.String(20), nullable=True)

    def _get_object(**kwargs):
        return Product(
            product_id=1,
            product_barcode="003",
            product_description="product3",
            product_category="Vegetal",
            product_type="Delicados",
            product_detail="product do campo",
            product_brand="",
            product_measure_unit="unit",
            product_fixed_margin="10222",
            product_status=True,
            product_retention_font="",
        )

    def to_object(self):
        return {
            "product_id": self.product_id,
            "product_barcode": self.product_barcode,
            "product_description": self.product_description,
            "product_category": self.product_category,
            "product_type": self.product_type,
            "product_detail": self.product_detail,
            "product_brand": self.product_brand,
            "product_measure_unit": self.product_measure_unit,
            "product_fixed_margin": self.product_fixed_margin,
            "product_status": self.product_status,
            "product_retention_font": self.product_retention_font,
            "product_date_added": self.product_date_added,
            "product_year_added": self.product_year_added,
            "product_month_added": self.product_month_added,
            "product_datetime_added": self.product_datetime_added,
            "product_date_updated": self.product_date_updated,
        }

    def get():
        """
        This method return all the products from the database
        """
        obj = Product.query.all()
        return True, obj

    # Create method
    def create_product(product=dict):
        """
        This method is used to save a product object
        into the database.

        Arguments:
            'product' -> is expected to be a dictionary with the product fields

        Return:
            By default the function returns a boolean and the product object if
            none error occured, if false return a boolean and an exception response
        """
        try:
            obj = Product(
                product_barcode=product["barcode"],
                product_description=product["description"],
                product_category=product["category"],
                product_type=product["type"],
                product_detail=product["detail"],
                product_brand=product["brand"],
                product_measure_unit=product["measure_unit"],
                product_fixed_margin=product["fixed_margin"],
                product_status=product["status"],
                product_retention_font=product["retention_font"],
                product_date_added=product["date_added"],
                product_year_added=product["year_added"],
                product_month_added=product["month_added"],
                product_datetime_added=product["datetime_added"],
            )
            db.session.add(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[createProduct]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        except IntegrityError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[createProduct]: \n \
                                       IntegrityError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, f"This product already exist. {str(e)}"
        except Exception as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[createProduct]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)

    # Update method
    def update_(product_id: int, product: dict) -> any:  # type: ignore
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
            obj = Product.query.filter(and_(Product.product_id == product_id)).first()
            obj.product_description = product["description"]
            obj.product_barcode = product["barcode"]
            obj.product_category = product["category"]
            obj.product_type = product["type"]
            obj.product_detail = product["detail"]
            obj.product_brand = product["brand"]
            obj.product_measure_unit = product["measure_unit"]
            obj.product_fixed_margin = product["fixed_margin"]
            obj.product_status = product["status"]
            obj.product_retention_font = product["retention_font"]
            obj.product_date_added = product["date_added"]
            obj.product_year_added = product["year_added"]
            obj.product_month_added = product["month_added"]
            obj.product_datetime_added = product["datetime_added"]

            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[update_]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
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
            set_logger_message(
                f"Error occured on method[update_]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)

    def update_product(product_id: int, **kwargs) -> any:  # type: ignore
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
        description = kwargs.get("description", None)
        barcode = kwargs.get("barcode", None)
        try:
            obj = Product.query.filter(and_(Product.product_id == product_id)).first()

            obj.product_description = (
                description if description is not None else obj.product_description
            )
            obj.product_barcode = (
                barcode if barcode is not None else obj.product_barcode
            )

            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[update_product]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
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
            set_logger_message(
                f"Error occured on method[update_product]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)

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
            obj = Product.query.filter_by(product_id=product_id).first_or_404()
            db.session.delete(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[delete_product]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
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
            set_logger_message(
                f"Error occured on method[delete_product]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
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
            obj = Product.query.all()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_all]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
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
            set_logger_message(
                f"Error occured on method[get_all]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)

    def get_by_id(id):
        """
        This method is used to filter all the products
        from the database by ID

        Return:
            It returns a boolean value and the product object
        """

        try:
            obj = Product.query.filter(and_(Product.product_id == id)).first()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_by_id]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
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
            set_logger_message(
                f"Error occured on method[get_by_id]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
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
            obj = Product.query.filter(
                and_(Product.product_barcode == barcode)
            ).first_or_404()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_by_barcode]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
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
            set_logger_message(
                f"Error occured on method[get_by_barcode]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)
        
    # Get Product by description
    def get_by_description(description):
        """
        This method is used to filter all the products
        from the database by description

        Return:
            It returns a boolean value and the product object
        """

        try:
            search_pattern = f"%{description}%"
            obj = Product.query.filter(
                and_(Product.product_description.like(search_pattern))
            ).all()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(
                f"Error occured on method[get_by_barcode]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
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
            set_logger_message(
                f"Error occured on method[get_by_barcode]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        "
            )
            return False, str(e)

    def convert_to_list(obj):
        objects = []
        for i, item in enumerate(obj):
            objects.append(
                {
                    "product_id": item.product_id,
                    "product_barcode": item.product_barcode,
                    "product_description": item.product_description,
                    "product_category": item.product_category,
                    "product_type": item.product_type,
                    "product_detail": item.product_detail,
                    "product_brand": item.product_brand,
                    "product_measure_unit": item.product_measure_unit,
                    "product_fixed_margin": item.product_fixed_margin,
                    "product_status": item.product_status,
                    "product_retention_font": item.product_retention_font,
                    "product_date_added": item.product_date_added,
                    "product_year_added": item.product_year_added,
                    "product_month_added": item.product_month_added,
                    "product_datetime_added": item.product_datetime_added,
                    "product_date_updated": item.product_date_updated,
                }
            )
        return objects
