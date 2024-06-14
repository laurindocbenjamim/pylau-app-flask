import os
import secrets
import pyotp

def set_app_config(app):   
    
    app.config['CORS_HEADERS'] = 'Content-Type'

    """
    The provided code is from a file called app_conf.py and it contains a line of code that sets the value of the OTP_SECRET_KEY variable using the os.getenv() function and secrets.token_urlsafe() function.

Let's break down the code step by step:

os.getenv('OTP', secrets.token_urlsafe(32)): This part of the code uses the os.getenv() function to retrieve the value of the environment variable named 'OTP'. If the environment variable is not found, it uses the secrets.token_urlsafe(32) function to generate a random URL-safe text string of length 32 as a default value.

OTP_SECRET_KEY = ...: This part assigns the value returned by os.getenv() to the OTP_SECRET_KEY variable.

To provide some context, the os.getenv() function is used to retrieve the value of environment variables in Python. Environment variables are system-specific values that can be accessed by programs running on the system. The secrets.token_urlsafe() function is used to generate a random URL-safe text string, which can be useful for generating secure tokens or keys.

In summary, the code retrieves the value of the environment variable 'OTP' using os.getenv(), and if the variable is not found, it generates a random URL-safe text string using secrets.token_urlsafe(). The resulting value is then assigned to the OTP_SECRET_KEY variable.


    """ 
    app.config.from_mapping(
        SECRET_KEY= os.getenv('SECRET_KEY', secrets.token_urlsafe(32)), # KEY GENERATED WITH secrets.token_urlsafe(32) 32 byts
        OTP_SECRET_KEY=os.getenv('OTP_SECRET_KEY', pyotp.random_base32()), 
    )

    # Set Email configurations
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'rocketmc2009@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jgtkeopkbwoxkjoo'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
