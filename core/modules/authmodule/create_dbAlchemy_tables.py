
from core.modules.authmodule.model.User import User
from ...config.sql_alchemy import dbAlch
from flask import current_app

def createTables():
    with current_app.app_context():
        dbAlch.create_all()
        #User.__table__.create(current_app.extensions['sqlalchemy'].engine)
        #return True
    #return False