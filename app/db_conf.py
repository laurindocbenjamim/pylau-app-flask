
import os
import secrets
from flask import current_app as m_app
from flask_cors import CORS
from flask_cors import cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# This function is used to connect to the local database
def connect_to_db_server(app,type_db=None):
    if type_db == 'mysql':
                   
        DATABASE_URI_1 = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'\
            .format(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_SERVER'), database=os.getenv('DB_NAME'))
        
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI_1
    elif type_db == 'postgres':
        local_db = "postgresql://postgres:root@localhost:5432/test"
        cloud_db = "postgres://fiysuzvofhprpp:ab6e8ad51efac658eca5c1b66056b9438d8866a522daeb3fee983b66970c0883@ec2-52-31-2-97.eu-west-1.compute.amazonaws.com:5432/db5veivij96r5u?sslmode=require"
        app.config["SQLALCHEMY_DATABASE_URI"] = cloud_db
        
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test3.db"

    
    """
    The line of code you provided is used to configure the behavior of SQLAlchemy, which is a popular Object-Relational Mapping (ORM) library for Python. 

In particular, [`app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FUtilizador%2FOneDrive%2FDocumentos%2FPythonProject%2FFlask-Projects%2Fpylau-app-flask%2Fapplication%2Fdb_conf.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A13%2C%22character%22%3A25%7D%5D "application/db_conf.py") is used to disable the SQLAlchemy's modification tracking feature. 

By default, SQLAlchemy tracks modifications made to objects and emits signals to inform the application about these changes. However, this feature can be resource-intensive and may not be necessary for all applications. 

Setting `SQLALCHEMY_TRACK_MODIFICATIONS` to `False` disables this tracking feature, which can improve performance in certain scenarios where modification tracking is not needed.
    """
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False        

    """
    GitHub Copilot
    used /explain (rerun without)
    The SQLALCHEMY_ECHO property is used in Python projects that utilize the SQLAlchemy library for database operations.

    When SQLALCHEMY_ECHO is set to True, SQLAlchemy will log all the SQL statements that are executed, along with other useful information, to the console. This can be helpful for debugging and understanding the interactions between your code and the database.

    By enabling SQLALCHEMY_ECHO, you can see the actual SQL queries being executed, which can be useful for troubleshooting issues such as incorrect or unexpected query results. It allows you to inspect the generated SQL statements and verify that they match your expectations.

    However, it's important to note that enabling SQLALCHEMY_ECHO in a production environment is not recommended, as it can have a negative impact on performance and may expose sensitive information. It is typically used during development and testing phases to gain insights into the database interactions.

    Here's an example of how SQLALCHEMY_ECHO can be used in a Flask application:
    """


    app.config["SQLALCHEMY_ECHO"] = True    
    
    """
    GitHub Copilot
    used /explain (rerun without)
    The SQLALCHEMY_POOL_RECYCLE property is used in Python projects that utilize the SQLAlchemy library for database operations. It specifies the number of seconds after which SQLAlchemy should recycle a database connection from the connection pool.

    When a connection is recycled, it means that SQLAlchemy will close the existing connection and create a new one. This is useful because database connections can become stale or unreliable over time, especially in long-running applications. By recycling connections, you can ensure that your application maintains a fresh and reliable connection to the database.

    The SQLALCHEMY_POOL_RECYCLE property takes an integer value representing the number of seconds. After this duration has passed since the connection was created or last used, SQLAlchemy will automatically recycle the connection. The default value is 3600 seconds (1 hour).

    Here's an example of how you can set the SQLALCHEMY_POOL_RECYCLE property in your db_conf.py file:

    By setting a reasonable value for SQLALCHEMY_POOL_RECYCLE, you can ensure that your application maintains a healthy connection pool and avoids potential issues caused by stale connections.

    """
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
    app.config['SQLALCHEMY_POOL_PRE_PING'] = True
    
    """
    app.config["SQLALCHEMY_BINDS"] = {
        'local': 'sqlite:///test3.db',
        'cloud': 'sqlite:///test4.db'
    }
    app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
    app.config["CORS_HEADERS"] = 'Content-Type'
    app.config["CORS_SUPPORTS_CREDENTIALS"] = True
    app.config["CORS_RESOURCES"] = {r"/api/*": {"origins": "*"}}
    app.config["CORS_EXPOSE_HEADERS"] = "Content-Type"
    app.config["CORS_ALLOW_HEADERS"] = "Content-Type"
    app.config["CORS_ALWAYS_SEND"] = True
    app.config["CORS_AUTOMATIC_OPTIONS"] = True
    app.config["CORS_SEND_WILDCARD"] = True
    app.config["CORS_MAX_AGE"] = 86400
    app.config["CORS_SEND_WILDCARD"] = True
    app.config["CORS_ALLOW_CREDENTIALS"] = True
    app.config["CORS_EXPOSE_HEADERS"] = "Content-Type"
    """


# This function is used to initialize the database
def init_db_server(app):
     # Init the db
    db.init_app(app)

    with app.app_context():
        db.create_all()

# This function is used to migrate the database
def migrate_db(app):
    Migrate(app, db)