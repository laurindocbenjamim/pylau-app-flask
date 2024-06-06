import pyotp

def generate_simple_otp(secret, accountname, interval):
    totp = pyotp.TOTP(secret,name=accountname, interval=interval)
    return totp

def check_simple_otp(OTP, secret, user, otp_time_interval):
    totp = generate_simple_otp(secret, user, otp_time_interval)     
    return totp.verify(OTP)

