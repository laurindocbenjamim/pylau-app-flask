
import secrets
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_caching import Cache
from flask_login import LoginManager

db = SQLAlchemy()

# This function is used to connect to the local database
def connect_to_server_db(app,type_db=None):
    if type_db == 'mysql':
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@localhost/testdb"
    elif type_db == 'postgres':
        local_db = "postgresql://postgres:root@localhost:5432/test"
        cloud_db = "postgres://fiysuzvofhprpp:ab6e8ad51efac658eca5c1b66056b9438d8866a522daeb3fee983b66970c0883@ec2-52-31-2-97.eu-west-1.compute.amazonaws.com:5432/db5veivij96r5u?sslmode=require"
        app.config["SQLALCHEMY_DATABASE_URI"] = cloud_db
        
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test2.db"

def create_app(config_filename, type_db=None, silent=True):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_pyfile(config_filename, silent=silent)
    secret = secrets.token_urlsafe(16)
    #app.secret_key = foo
    app.config.from_mapping(
        SECRET_KEY=secret
    )
    app.config['CACHE_TYPE'] = 'simple'  # Choose cache type, e.g., 'simple', 'redis', etc.
    
    CORS(app)

    connect_to_server_db(app,type_db)

    # Login Manager is needed for the the application 
    # to be able to log in and log out users

    login_manger = LoginManager()
    #login_manger.login_view = 'auth.user.login'
    login_manger.init_app(app)
    

    #from model.usermodel import db

    # Initialize the application extension
    db.init_app(app)
    
    # Create the database within the app context
    with app.app_context():
        db.create_all()


    # Main route
    @app.route('/')
    def index():
        return render_template('site_home.html')
    
    from .views.error_handlers_view import error_handlers_view
    error_handlers_view(app)

    # Integrating the blueprints parent and child into the application
    from .views.bp_auth_register_view import bp_auth_parent, init_app as init_app_register
    from .views.bp_auth_login_view import bp_auth_login_child, init_app as init_app_login
    init_app_register(login_manger)
    init_app_login(login_manger, db=db)
    bp_auth_parent.register_blueprint(bp_auth_login_child)
    app.register_blueprint(bp_auth_parent)

    # Integrating the blueprints into the application
    from .views.bp_main_view import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .views.bp_select_view import bp as select_bp, init_select_view_app
    #@cache.cached(timeout=50)
    init_select_view_app(login_manger)
    app.register_blueprint(select_bp)

    from . views.bp_create_user_view import bp as create_bp, init_app
    init_app(login_manger, db=db)
    app.register_blueprint(create_bp)

   

    
    
    #from model.usermodel import User

    # Import the views

    #from views.rootViews.homeView import HomeView
    #app.add_url_rule('/', view_func=HomeView.as_view('home_view'))

    #from views.userViews.UserListView import UserListView
    #app.add_url_rule('/users/', view_func=UserListView.as_view('user_view'))


    #from views.selectViews.listView import ListView
    #app.add_url_rule('/list/users/', view_func=ListView.as_view('user_list_view', User, 'list.html'))
    

    # Init the migration

    migrate = Migrate(app, db)

    return app