import pyotp
import time

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
    totp = pyotp.TOTP(secret)
    return totp.now()

# Verify OTP using the secret key
def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)    
    return totp.verify(otp)

# Get time remaining for OTP to expire
def get_time_remaining(secret):
    totp = pyotp.TOTP(secret)
    return 30 - (int(time.time()) % 30) 


secret = generate_secret()

otp = generate_otp(secret)
print(otp)

#time.sleep(30)
print(f" Time: {get_time_remaining(secret)}")
print(verify_otp(secret, otp))

