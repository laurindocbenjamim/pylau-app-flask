

import pyotp


# Generate a random secret key
def generate_secret():
    return pyotp.random_base32()

def get_otp(secret, accountname, interval):
    totp = pyotp.TOTP(secret,name=accountname, interval=interval)
    return totp

def check_otp(OTP, secret, user, otp_time_interval):
    totp = get_otp(secret, user, otp_time_interval)     
    return totp.verify(OTP)
