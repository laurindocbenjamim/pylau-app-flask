import os

class Config:
    DEBUG = False
    TESTING = False
    SMTP_HOST = os.environ.get('SMTP_HOST') 
    SMTP_PORT = os.environ.get('SMTP_PORT')# 587 by default
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    DB_SERVER = os.environ.get('DB_SERVER')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_POOL_PRE_PING = True
    

    @property
    def DATABASE_URI(self):  # Note: all caps
        return f"mysql://user@{self.DB_SERVER}/foo"

class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:///test3.db"
    DEBUG = True
    SMTP_HOST = os.environ.get('SMTP_HOST') 
    SMTP_PORT = os.environ.get('SMTP_PORT')# 587 by default
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SECRET_KEY= os.getenv('SECRET_KEY') # KEY GENERATED WITH secrets.token_urlsafe(32) 32 byts
    OTP_SECRET_KEY= os.getenv('OTP_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_POOL_PRE_PING = True


    
    def __init__(self, database_type = 'sqlite') -> None:
        super().__init__()
        self.database_type = database_type
        
        self.load_database_config()

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.DATABASE_URI
    
    def load_database_config(self):
        if self.database_type == 'mysql':            
            # Create the URI for the local database
            DATABASE_URI_LOCAL = 'mysql://{}:{}@{}:{}/{}'.format(
                os.getenv('MYSQL_DB_USER'), 
                os.getenv('MYSQL_DB_PASSWORD'), 
                os.getenv('MYSQL_DB_SERVER'), 
                os.getenv('MYSQL_DB_PORT'), 
                os.getenv('MYSQL_DB_NAME')
            )
            # Set the URI Database configuration to the main app URI database
            self.DATABASE_URI = DATABASE_URI_REMOTE.replace(' ', '').replace('\n','')
        
        elif self.database_type == 'remote-mysql':
            # Create the URI for the remote database
            DATABASE_URI_REMOTE = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
                os.getenv('DB_USER'), 
                os.getenv('DB_PASSWORD'),
                os.getenv('DB_SERVER'), 
                os.getenv('DB_PORT'), 
                os.getenv('DB_NAME')
            )
            
            # Set the URI Database configuration to the main app URI database
            self.DATABASE_URI = DATABASE_URI_REMOTE.replace(' ', '').replace('\n','')

        elif self.database_type == 'postgres':
            DATABASE_URI_HEROKU = 'postgresql://{}:{}@{}:{}/{}'.format(
                os.getenv('DB_USER'), 
                os.getenv('DB_PASSWORD'), 
                os.getenv('DB_SERVER'), 
                os.getenv('DB_PORT'), 
                os.getenv('DB_NAME')
            )
            # Set the URI Database configuration to the main app URI database
            self.DATABASE_URI = DATABASE_URI_HEROKU.replace(' ', '').replace('\n','')

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'