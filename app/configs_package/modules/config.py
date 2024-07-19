import os

class Config:
    DEBUG = False
    TESTING = False
    WATSON_NP_API_URI = os.environ.get('WATSON_NP_API_URI') 
    WATSON_NP_API_KEY = os.environ.get('WATSON_NP_API_KEY')
    SMTP_HOST = os.environ.get('SMTP_HOST') 
    SMTP_PORT = os.environ.get('SMTP_PORT')# 587 by default
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    DB_SERVER = os.environ.get('DB_SERVER')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_POOL_PRE_PING = True
    UPLOAD_FOLDER = 'app/static/uploads/'
    

    @property
    def DATABASE_URI(self):  # Note: all caps
        return f"mysql://user@{self.DB_SERVER}/foo"


"""
CLASS  USED ON DEVELOPMENT MODE
"""
class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:///test3.db"
    UPLOAD_FOLDER = 'app/static/uploads/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'}
    DEBUG = True
    WATSON_NP_API_URI = os.environ.get('WATSON_NP_API_URI') 
    WATSON_NP_API_KEY = os.environ.get('WATSON_NP_API_KEY')
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
        if self.database_type is not None and self.database_type == 'mysql':            
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
        
        elif self.database_type is not None and self.database_type == 'remote-mysql':
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

        elif self.database_type is not None and self.database_type == 'postgres':
            DATABASE_URI_HEROKU = 'postgresql://{}:{}@{}:{}/{}'.format(
                os.getenv('DB_USER'), 
                os.getenv('DB_PASSWORD'), 
                os.getenv('DB_SERVER'), 
                os.getenv('DB_PORT'), 
                os.getenv('DB_NAME')
            )
            # Set the URI Database configuration to the main app URI database
            self.DATABASE_URI = DATABASE_URI_HEROKU.replace(' ', '').replace('\n','')


"""
CLASS USED ON TEST MODE
"""
class TestingConfig(Config):
    TESTING = True    
    DATABASE_URI = "sqlite:///test.db"
    UPLOAD_FOLDER = 'app/static/uploads/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'}
    WATSON_NP_API_URI = os.environ.get('WATSON_NP_API_URI') 
    WATSON_NP_API_KEY = os.environ.get('WATSON_NP_API_KEY')
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
    
    def __init__(self) -> None:
        super().__init__()
        #DATABASE=os.path.join(app.instance_path, 'app.sqlite'),

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.DATABASE_URI

"""
CLASS  USED ON PRODUCTION MODE
"""
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    UPLOAD_FOLDER = 'app/static/uploads/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'}