import pyotp
import datetime
import qrcode
import os
from flask import url_for
from core import TwoFAModel

""" The  generate_secret  function generates a random secret key 
    that is used to generate the OTP. The  generate_otp  function 
    generates the OTP using the secret key. The  verify_otp  function 
    verifies the OTP using the secret key. The  get_time_remaining  
    function returns the time remaining for the OTP to expire.
"""

# create a User
def save_data(db, user_id, two_factor_auth_secret, method_auth):
    object = TwoFAModel( 
        userID = user_id,
        two_factor_auth_secret = two_factor_auth_secret, 
        method_auth = method_auth 
    )
    db.session.add(object)
    db.session.commit()
    return object


# Generate a random secret key
def generate_secret():
    return pyotp.random_base32()

# returns a 40-character hex-encoded secret
def hex_encoded(secret):
    return pyotp.random_hex()  

# Generate OTP using the secret key
def generate_otp(secret, accountname='username', interval=40):
    totp = pyotp.TOTP(secret,name=accountname, interval=interval)
    return totp

# Verify OTP using the secret key
def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)    
    return totp.verify(otp)

# Get time remaining for OTP to expire
def get_time_remaining(secret):
    totp = pyotp.TOTP(secret)
    time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
    return time_remaining 


def get_otp_code(secret, accountname='username', interval=40):
    totp = pyotp.TOTP(secret,name=accountname, interval=interval)

    codenow = totp.now()
    #print(codenow)

    #code = int(input("Enter the OTP: "))

    #print(verify_otp(secret, code))
    return codenow

def check_otp_code(secret, code):
    totp = pyotp.TOTP(secret)
    resp = totp.verify(code)
    return resp

def generate_provisioning_uri(secret, accountname='username'):
    otpuri = pyotp.totp.TOTP(secret).provisioning_uri(name=accountname, issuer_name='PyLau App')
    #code = pyotp.random_base32()
    imagename = secret +'-otpqrcode.png'
    qrcode.make(otpuri).save('core/static/otp_qrcode_images/'+imagename)
    return imagename

def verify_provisioning_uri(secret, code):
    totp = pyotp.TOTP(secret)
    resp = totp.verify(code)
    return resp

def update_imagename(image_path, new_imagename):
    # Get the directory path of the image
    directory = os.path.dirname(image_path)
            
    # Get the extension of the image
    extension = os.path.splitext(image_path)[1]
            
            # Create the new image path with the updated imagename
    new_image_path = os.path.join(directory, new_imagename + extension)
            
    # Rename the image file
    os.rename(image_path, new_image_path)
            
    return new_image_path

def remove_files_from_root_folder():
    root_folder = os.getcwd()
    files = os.listdir(root_folder)
        
    for file in files:
        file_path = os.path.join(root_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        
    return "Files removed from root folder."



    

   
   

