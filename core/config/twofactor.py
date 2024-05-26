import pyotp
import datetime

""" The  generate_secret  function generates a random secret key 
    that is used to generate the OTP. The  generate_otp  function 
    generates the OTP using the secret key. The  verify_otp  function 
    verifies the OTP using the secret key. The  get_time_remaining  
    function returns the time remaining for the OTP to expire.
"""

# Generate a random secret key
def generate_secret():
    return pyotp.random_base32()

# returns a 40-character hex-encoded secret
def hex_encoded(secret):
    return pyotp.random_hex()  

# Generate OTP using the secret key
def generate_otp(secret):
    totp = pyotp.TOTP(secret,name='Laurindo', interval=30)
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


def get_otp(secret):
    #secret = generate_secret()

    otp = generate_otp(secret)

    codenow = otp.now()
    #print(codenow)

    #code = int(input("Enter the OTP: "))

    #print(verify_otp(secret, code))
    return otp

def check_otp(secret, code):
    resp = verify_otp(secret, code)
    return resp
   

