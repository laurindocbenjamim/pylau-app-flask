


import os
import secrets
from datetime import datetime, timedelta
from flask_wtf import CSRFProtect
from flask_caching import Cache
from flask import Flask, request, session, jsonify, render_template
from quart import Quart, render_template, websocket
from flask import make_response
from flask_cors import CORS, cross_origin
from flask_talisman import Talisman
from flask_migrate import Migrate
from flask_login import LoginManager
from .configs_package import DevelopmentConfig, TestingConfig, ProductionConfig

from .configs_package.modules.load_database import db

#Importing the mongoDB library
from flask_pymongo import PyMongo
mongo_connection = None


"""

"""
def create_app(JDBC="sqlite",test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    

    """
    These options can be added to a Set-Cookie header to improve their security. Flask has 
    configuration options to set these on the session cookie. 
    They can be set on other cookies too.
    """
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
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
    
    if test_config is None:
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
    
    CORS(app)
    #app.secret_key = '20CHiteECulO081190#'
    csrf = CSRFProtect(app=app)
    

    #
    cache = Cache(app)
    #cacheQuizz = Cache(config={'CACHE_TYPE': 'CourseContentQuizz'})
    #cacheQuizz.init_app(app)
    #
    #Quart(app)

    # Create the mongodb instance
    global mongo_connection # Convert the 'mongo_connection' variable to GLOBAL
    mongo_connection = PyMongo(app)
   
    # Login Manager is needed for the the application 
    # to be able to log in and log out users

    login_manager = LoginManager()
    login_manager.init_app(app)
    #login_manager.login_view = 'auth.user.login'

    # import and call the database configuration
    from app.configs_package.modules.load_database import init_db_server  
    init_db_server(app)

    #from .routes import load_routes
    #from .configs_package.views.routes import load_routes
    from .utils.views.routes import load_routes
    load_routes(app=app, db=db, login_manager=login_manager)
    
    
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