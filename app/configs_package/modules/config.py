import os

from datetime import timedelta
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_jwt_extended import JWTManager
from app.dependencies import LoginManager
from flask_seasurf import SeaSurf  # CSRF Protection
from authlib.integrations.flask_client import OAuth
from app.dependencies import Cache, Limiter, get_remote_address

csrf=CSRFProtect()
# Apply JWT authentication
jwt = JWTManager()
login_manager = LoginManager()
# Initialize CSRF protection
#csrf = SeaSurf()
oauth = OAuth()
cache = Cache()

limiter = Limiter(key_func=get_remote_address, default_limits=["300 per day", "100 per hour"])

class Config:
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    HTTP_ONLY=True
    
    SAME_SITE="Strict"
    SESSION_TYPE= 'filesystem'    

    SECRET_KEY= os.getenv('SECRET_KEY') # KEY GENERATED WITH secrets.token_urlsafe(32) 32 byts
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # Token locations
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    # Cookie names
    JWT_ACCESS_CSRF_COOKIE_NAME = 'csrf_access_token'
    JWT_REFRESH_CSRF_COOKIE_NAME = 'csrf_refresh_token'
    # Cookie settings
    JWT_COOKIE_SECURE = True # Requires HTTPS in production
    JWT_COOKIE_HTTPONLY = True # Prevent JavaScript access
    JWT_COOKIE_SAMESITE = 'Lax' # Strict same-site policy
    """
    Strict to maximize security and avoid your JWTs being included in any cross-site requests.
    Lax if your app has login flows that involve external sites (e.g., OAuth login).
    """
    JWT_SESSION_COOKIE = False  # Different from session cookies
    JWT_CSRF_CHECK_FORM = True      # Enable CSRF protection for form submissions
    # Expiration times
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

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
    MAX_CONTENT_LENGTH=50 * 1024 * 1024 # 16 MB limit for file uploads
    UPLOAD_FOLDER = 'uploads'
    UPLOAD_FOLDER_TEMP = 'temp'
    FILES_FOLDER = 'files'
    UPLOAD_VIDEO_FOLDER= 'videos'
    UPLOAD_DOCS_FOLDER= 'docs'
    DECRYPTED_FOLDER = 'decrypted'
    MODIFIED_FOLDER = 'modified'
   
    SPACE_SECRET_KEY=os.environ.get('SPACE_SECRET_KEY')#NAME: ID:
    SPACE_ACCESS_KEY=os.environ.get('SPACE_ACCESS_KEY')
    SPACE_API_ENDPOINT='https://data-tuning.storage.nyc3.digitaloceanspaces.com'
    BUCKET_NAME='access-key-read-write-1738172573872'
    UPLOAD_FOLDER_PERMISSIONS='0755'
    ALLOWED_EXTENSIONS = {'txt', '.pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'webm', 'mkv', 'avi'}
    UPLOAD_EXTENSION_DOCS_ALLOWED = ['.pdf', '.docx', '.csv', '.txt']
    UPLOAD_EXTENSIONS_IMAGE_ALLOWED = ['.jpg','.jpeg', '.png', '.gif']
    UPLOAD_EXTENSIONS_VIDEO_ALLOWED = ['.mp4', '.mkv', '.wave']

    @property
    def DATABASE_URI(self):  # Note: all caps
        return f"mysql://user@{self.DB_SERVER}/foo"


"""
CLASS  USED ON DEVELOPMENT MODE
"""
class DevelopmentConfig(Config):
 
    DATABASE_URI = "sqlite:///dtuning.db"

     # Configuration for MongoDB
    user="root"
    password ="root"
    host ="localhost"
    MONGO_URI = str(os.environ.get('MONGO_URI')).replace('"','')

    CACHE_TYPE = 'simple' 
    
    DEBUG = False
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

        self.MONGO_URI = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName=Cluster0".format(
            os.getenv('MONGO_DB_USER'),
            os.getenv('MONGO_DB_PASSWORD'),
            os.getenv('MONGO_DB_HOST'),
            os.getenv('MONGO_DB_NAME')
            )

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

        else:
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
    
    DATABASE_URI = "sqlite:///dataframe.db"
    # Configuration for MongoDB
    user="root"
    password ="root"
    host ="localhost"
    MONGO_URI = "mongodb://localhost:27017/course"
    
    WATSON_NP_API_URI = os.environ.get('WATSON_NP_API_URI') 
    WATSON_NP_API_KEY = os.environ.get('WATSON_NP_API_KEY')

    CACHE_TYPE = 'simple' 

    SMTP_HOST = os.environ.get('SMTP_HOST') 
    SMTP_PORT = os.environ.get('SMTP_PORT')# 587 by default
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    
    OTP_SECRET_KEY= os.getenv('OTP_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_POOL_PRE_PING = True
    
    def __init__(self) -> None:
        super().__init__()
        self.MONGO_URI = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority&appName=Cluster0".format(
            os.getenv('MONGO_DB_USER'),
            os.getenv('MONGO_DB_PASSWORD'),
            os.getenv('MONGO_DB_HOST'),
            os.getenv('MONGO_DB_NAME')
            )
        #DATABASE=os.path.join(app.instance_path, 'app.sqlite'),

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.DATABASE_URI

"""
CLASS  USED ON PRODUCTION MODE
"""
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    