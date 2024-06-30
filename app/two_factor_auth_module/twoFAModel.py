import os
import traceback
import sys
import pyotp
import datetime
import qrcode
from flask import current_app
from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import and_
from app.configs_package.modules.db_conf import db
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from ..configs_package.modules.logger_config import get_message as set_logger_message

class TwoFAModel(db.Model):
    """
    This class represents the model for two-factor authentication in the application.
    It defines the database table 'two_fa_auth' and provides methods for generating and verifying one-time passwords (OTP).
    """

    __tablename__ = 'two_fa_auth'
    two_fa_id:Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)
    userID:Mapped[int] = db.Column(db.Integer, nullable=False, unique=False)
    two_factor_auth_secret:Mapped[str] = db.Column(db.String(100), unique=False, nullable=False)  
    method_auth:Mapped[str] = db.Column(db.String(20),default="app", nullable=False) 
    is_active:Mapped[str] = db.Column(db.Boolean(), default=True, nullable=True)
    date_added = db.Column(db.Date(), default=datetime.now().date())
    datetime_added = db.Column(db.DateTime, default=datetime.now())
    date_exp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc) + timedelta(days=1))
    
    def __repr__(self):
        return f'<TwoFAModel {self.two_fa_id} - {self.userID}>'
    
    def to_dict(self):
        return {
            'two_fa_id': self.two_fa_id,
            'userID': self.userID,
            'two_factor_auth_secret': self.two_factor_auth_secret,
            'method_auth': self.method_auth,
            'date_added': self.date_added
        }

    def save_two_fa_data(obj):
        """
        Saves the TwoFAModel object to the database.

        Args:
            obj: The TwoFAModel object to be saved.

        Returns:
            A tuple containing a boolean indicating the success of the operation and the saved object.
        """
        try:
            db.session.add(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[save_two_fa_data]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[save_two_fa_data]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            return False, str(e)
    
    def update_secret_two_fa_data(user_id):
        """
        Updates the secret key for two-factor authentication in the database.

        Args:
            user_id: The ID of the user.

        Returns:
            A tuple containing a boolean indicating the success of the operation and the updated object.
        """
        try:
            obj = TwoFAModel.query.filter_by(userID=user_id).first_or_404()
            obj.two_factor_auth_secret = pyotp.random_base32()
            db.session.merge(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[update_secret_two_fa_data]: \n \
                                       SQLAlchemyError: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            set_logger_message(f"Error occured on method[update_secret_two_fa_data]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ") 
            return False, str(e)
        
    def update_two_fa_data(obj):
        """
        Updates the TwoFAModel object in the database.

        Args:
            obj: The TwoFAModel object to be updated.

        Returns:
            A tuple containing a boolean indicating the success of the operation and the updated object.
        """
        try:
            db.session.merge(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_two_fa_data]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            set_logger_message(f"Error occured on METHOD[update_two_fa_data]: \n Exception: {str(e)}")
            return False, str(e)
    


    def delete_two_fa_data(obj):
        """
        Deletes the TwoFAModel object from the database.

        Args:
            obj: The TwoFAModel object to be deleted.

        Returns:
            A tuple containing a boolean indicating the success of the operation and the deleted object.
        """
        try:
            db.session.delete(obj)
            db.session.commit()
            return True, obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            return False, str(e)
        
    def  get_all_two_fa_data():
        """
        Retrieves all two-factor authentication data from the database.

        Returns:
            A list of all two-factor authentication data.
        """
        return TwoFAModel.query.all()
    

    
    def  get_user_two_fa_data(user_id):
        """
        Retrieves the two-factor authentication data for the given user.

        Args:
            user_id: The ID of the user.

        Returns:
            The two-factor authentication data for the user.
        """
        try:
            obj = TwoFAModel.query.filter_by(userID=user_id).first_or_404()
            return True, obj
        except SQLAlchemyError as e:
            set_logger_message(f"Error occured on METHOD[get_user_two_fa_data]: \n SQLAlchemyError: {str(e)}")
            return False, str(e)
        except Exception as e:
            set_logger_message(f"Error occured on METHOD[get_user_two_fa_data]: \n Exception: {str(e)}")
            return False, str(e)
    
    def  get_user_two_fa_by_id(two_fa_id):
        """
        Retrieves the two-factor authentication data for the given 2-FA.

        Args:
            two_fa_id: The ID of the 2-FA object.

        Returns:
            The two-factor authentication data for the user.
        """
        return TwoFAModel.query.filter_by(two_fa_id=two_fa_id).first_or_404()

    def  get_user_two_fa_by_secret(secret):
        """
        Retrieves the two-factor authentication data for the given secret key.

        Args:
            secret: The secret key for two-factor authentication.

        Returns:
            The two-factor authentication data for the user.
        """
        return TwoFAModel.query.filter_by(two_factor_auth_secret=secret).first_or_404()
    
    def generate_secret():
        """
        Generates a random secret key for two-factor authentication.

        Returns:
            A randomly generated secret key.
        """
        return pyotp.random_base32()


    def generate_otp(**kwargs):
        """
        Generates a one-time password (OTP) for the given account.

        Args:
            kwargs:
                - accountname: The name of the account.
                - secret: The secret key for two-factor authentication.
                - interval: The time interval for the OTP.

        Returns:
            The generated OTP.
        """
        accountname = kwargs.get('accountname')
        secret = current_app.config['OTP_SECRET_KEY']
        interval = kwargs.get('interval')

        totp = pyotp.TOTP(secret,name=accountname, interval=interval)
        return totp

    def generate_provisioning_uri(**kwargs):
        imagename = None
        """
        Generates a provisioning URI for the given account.

        Args:
            kwargs:
                - accountname: The name of the account.
                - secret: The secret key for two-factor authentication.

        Returns:
            The name of the generated QR code image.
        """
        accountname = kwargs.get('accountname')
        secret = current_app.config['OTP_SECRET_KEY']
        otpuri = pyotp.totp.TOTP(secret).provisioning_uri(name=accountname, issuer_name='DTuning App')
    
        imagename = secret +'-otpqrcode.png'
        qrcode.make(otpuri).save('app/static/otp_qrcode_images/'+imagename)
        #set_logger_message(f"Error occured on METHOD[save_two_fa_data]: \n SQLAlchemyError: {str(e)}")
        return imagename

    def verify_provisioning_uri(**kwargs):
        """
        Verifies the provisioning URI with the given secret key and code.

        Args:
            kwargs:
                - secret: The secret key for two-factor authentication.
                - code: The code to be verified.

        Returns:
            True if the code is valid, False otherwise.
        """
        secret = current_app.config['OTP_SECRET_KEY']
        code = kwargs.get('code')
        
        totp = pyotp.TOTP(secret)
        if totp.verify(code):
            return True
        return False
    

    def update_imagename(image_path, new_imagename):
        try:
            # Get the directory path of the image
            directory = os.path.dirname(image_path)
                    
            # Get the extension of the image
            extension = os.path.splitext(image_path)[1]
                    
                    # Create the new image path with the updated imagename
            new_image_path = os.path.join(directory, new_imagename + extension)
                    
            # Rename the image file
            os.rename(image_path, new_image_path)
                    
            return new_image_path
        except Exception as e:
            return False
    