

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#db = SQLAlchemy()

def create_app(config_filename, silent=True):
    app = Flask(__name__, template_folder='templates')
    app.config.from_pyfile(config_filename, silent=silent)

    #from model.usermodel import db

    # Init the db
    #db.init_app(app)

    #with app.app_context():
        #db.create_all()
    
    from model.usermodel import User

    from views.rootViews.homeView import HomeView
    app.add_url_rule('/', view_func=HomeView.as_view('home_view'))

    from views.userViews.UserListView import UserListView
    app.add_url_rule('/users/', view_func=UserListView.as_view('user_view'))


    from views.selectViews.listView import ListView
    app.add_url_rule('/list/users/', view_func=ListView.as_view('user_list_view', User, 'list.html'))
    

    # Init the migration

    #migrate = Migrate(app, db)

    return app