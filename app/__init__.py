
# This file is the entry point of the application. It is the file that will be run to start the application.
import redis

# Import the necessary modules
from app.dependencies import os
from app.dependencies import datetime
from app.dependencies import timedelta

#from app.dependencies import CSRFProtect
#from flask_wtf.csrf import CSRFProtect, generate_csrf
from app.dependencies import Cache
from app.dependencies import Flask
from app.dependencies import request    
from app.dependencies import jsonify
from app.dependencies import render_template
from app.dependencies import make_response
from app.dependencies import CORS
from app.dependencies import cross_origin, ProxyFix
from app.dependencies import LoginManager
from app.dependencies import Limiter
from app.dependencies import PyMongo
from app.dependencies import get_remote_address
from app.dependencies import Api
from app.api.auth.login_rest_api import User
from app.api.auth.token_block_list import TokenBlocklist

# Import the configuration classes
from app.configs_package import DevelopmentConfig, TestingConfig, ProductionConfig 
from app.configs_package import csrf, jwt, oauth, cache, limiter, login_manager

from app.configs_package.modules.load_database import init_db_server  # Import the database configuration
from app.configs_package.modules.load_database import db
from app.routes import load_routes
from app.blue_prints import load_blueprints
from app.utils.cors_police import allowed_domains_to_upload_route, allowed_domains_to_api_route, allowed_domains_to_files_route

# Create and configure the app
app = Flask(__name__, instance_relative_config=True)
#pp.config['REDIS_URL'] = "redis://localhost:6379/0"

#redis_client = redis.Redis.from_url(app.config['REDIS_URL'])
#limiter = Limiter(key_func=get_remote_address, default_limits=["300/day", "200/hour"], storage_uri="redis://localhost:6379/0")
#limiter = Limiter(key_func=get_remote_address, default_limits=["300/day", "200/hour"])

#login_manager = LoginManager()
"""

"""
def create_app(JDBC="sqlite",test_config=None):
    
    
    #api = Api(app)

    """
    These options can be added to a Set-Cookie header to improve their security. Flask has 
    configuration options to set these on the session cookie. 
    They can be set on other cookies too.
    """
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        #SESSION_COOKIE_SAMESITE='Lax',
        #PERMANENT_SESSION_LIFETIME=600,
    )

    # Flask-Talisman is an extension that simplifies the process of adding security headers, including CSP, to your Flask application.
    # https://github.com/GoogleCloudPlatform/flask-talisman
    """Talisman(app, content_security_policy={
        'default-src': ['\'self\''],
        'img-src': ['\'self\'', 'data:'],
        'script-src': ['\'self\'', 'https://trustedscripts.example.com'],
        'style-src': ["'self'"]
    })"""
    
    if not test_config or test_config is None:
        # Load  the  instance config if it exists, when not testing
        #app.config.from_pyfile('config.py', silent=True)
        app.config.from_object(DevelopmentConfig(JDBC))
    else:
        # Load the test config if passed in
        #app.config.from_mapping(test_config)
        app.config.from_object(TestingConfig())

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Create directories
    os.makedirs(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['UPLOAD_VIDEO_FOLDER']), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['UPLOAD_DOCS_FOLDER']), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['DECRYPTED_FOLDER']), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['MODIFIED_FOLDER']), exist_ok=True)


    # Create permition
    os.chmod(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['UPLOAD_VIDEO_FOLDER']), 0o755)
    os.chmod(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['UPLOAD_DOCS_FOLDER']), 0o755)
    os.chmod(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['DECRYPTED_FOLDER']), 0o755)
    os.chmod(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER'], app.config['MODIFIED_FOLDER']), 0o755)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    CORS(app,resources={
        r"/videos/post": {"origins": allowed_domains_to_upload_route()},
        r"/upload": {"origins": allowed_domains_to_upload_route()},
        r"/api/csrf-token/get": {"origins": allowed_domains_to_upload_route()},
        r"/api/upload": {"origins": allowed_domains_to_upload_route()},
        r"/api/files-storage": {"origins": allowed_domains_to_files_route()},
        r"/api/*": {"origins": allowed_domains_to_api_route()},
        r"/api-auth/*": {"origins": allowed_domains_to_api_route ()},
        #r"/api-auth/protected": {"origins": allowed_domains_to_api_route ()},
    },supports_credentials=True)
    
    #csrf = CSRFProtect(app=app)
   
    csrf.init_app(app=app)
    jwt.init_app(app=app)
    oauth.init_app(app=app)
    # Apply security middlewares 
    app.wsgi_app = ProxyFix(app.wsgi_app)
    #cache = Cache(app)
    cache.init_app(app=app)
    #cacheQuizz = Cache(config={'CACHE_TYPE': 'CourseContentQuizz'})
    #cacheQuizz.init_app(app)
    # Login Manager is needed for the the application 
    # to be able to log in and log out users
    
    login_manager.init_app(app)
    #
    #Quart(app)

    # Create the mongodb instance
    #global mongo_connection # Convert the 'mongo_connection' variable to GLOBAL
    #mongo_connection = PyMongo(app)
   
    
    
    #login_manager.login_view = 'auth.user.login'

    # import and call the database configuration
    
    init_db_server(app)
    
    limiter.init_app(app)

    from app.utils.views.error_handlers_view import error_handlers_view
    error_handlers_view(app)

    #from .routes import load_routes
    #from .configs_package.views.routes import load_routes
    #from app.utils.views.routes import load_routes
    # Load the routes
    load_routes(app=app, db=db, login_manager=login_manager, limiter=limiter)

    # Load the blueprints
    load_blueprints(app=app, db=db, login_manager=login_manager, limiter=limiter)
    
    

    # Create a sitemap route
    @app.route("/sitemap.xml")
    @cross_origin(methods=["GET"])
    def sitemap():
        base_url = request.url_root
        try:
            """ Generating a sitemap.xml 
            Makes a list of URL and dates modified.
            """
            pages = []
            ten_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()

            # Static pages 
            for rule in app.url_map.iter_rules():
                if "GET" in rule.methods and len(rule.arguments)==0:
                    pages.append(
                        [request.url_root + str(rule.rule), ten_days_ago]
                    )
            sitemap_xml = render_template('sitemap_template.xml', pages=pages)
            response = make_response(sitemap_xml)
            response.headers["Content-Type"] = "application/xml"
            return response
        except Exception as e:
            return str(e)


    # Simple page that say hello
    @app.route('/test-mongo')
    @limiter.limit("1 per hour", error_message='chill!')
    def test():
       
        """ collection = mongo_connection.db.courses
        data = collection.find()
    
        return f' CONNECT {app.config['MONGO_URI']}'"""
        from pymongo import MongoClient
        from flask import current_app

        #create the connection url
        #connecturl = "mongodb://{}:{}@{}:27017/?authSource=course".format(os.getenv,password,host)
        #connecturl = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&appName=Cluster0".format(user,password,host)#"mongodb+srv://rocketmc2009:<db_password>@cluster0.s2tvs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        connecturl = current_app.config['MONGO_URI']
        # connect to mongodb server
        
        connection = MongoClient(current_app.config['MONGO_URI'])
        # get database list
        
        dbs = connection.list_database_names()
        return jsonify(dbs)
    return app




# JWT configuration
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

# CSRF error token handling
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"error": "Missing authorization token"}), 401

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))