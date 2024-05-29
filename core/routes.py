
"""
In this file, we will define the routes for our application.
"""

# Importing the required libraries
from flask import render_template, request, redirect, url_for, jsonify
#from app import Person
from core import Person
from core import create_person, get_all_people, get_person_by_id

# Import all routes
from core.homemodule.routes import home_routes
from core.personmodule.personroutes import person_routes
from core.devmodule.routes import dev_routes

def run_routes(app, db):

    home_routes(app, db)

    person_routes(app, db)

    dev_routes(app, db)






