import os

class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY= os.getenv('SECRET_KEY'), # KEY GENERATED WITH secrets.token_urlsafe(32) 32 byts
    OTP_SECRET_KEY= os.getenv('OTP_SECRET_KEY'), 
    

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'