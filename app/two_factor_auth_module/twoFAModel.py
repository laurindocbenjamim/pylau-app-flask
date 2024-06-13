import os
import pyotp
import datetime
import qrcode
from sqlalchemy.orm import Mapped,mapped_column, relationship

from app import db
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError

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
    date_added = db.Column(db.DateTime, default=datetime.now())
    date_exp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc) + timedelta(days=30))
    
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
            return False, str(e)
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    

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
        secret = kwargs.get('secret')
        interval = kwargs.get('interval')

        totp = pyotp.TOTP(secret,name=accountname, interval=interval)
        return totp

    def generate_provisioning_uri(**kwargs):
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
        secret = kwargs.get('secret')
        otpuri = pyotp.totp.TOTP(secret).provisioning_uri(name=accountname, issuer_name='PyLau App')
    
        imagename = secret +'-otpqrcode.png'
        qrcode.make(otpuri).save('app/static/otp_qrcode_images/'+imagename)
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
        secret = kwargs.get('secret')
        code = kwargs.get('code')
        
        totp = pyotp.TOTP(secret)
        resp = totp.verify(code)
        return resp
    

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
    