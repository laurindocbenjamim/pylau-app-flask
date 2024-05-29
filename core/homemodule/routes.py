
"""
In this file, we will define the routes for our application.
"""

# Importing the required libraries
from flask import render_template, request, redirect, url_for, jsonify
#from app import Person
from core import Person
from core import create_person, get_all_people, get_person_by_id

def home_routes(app, db):
    
    @app.route('/', methods=['GET'])
    def index():
        return  render_template('home2.html')


