
"""
In this file, we will define the routes for our application.
"""

# Importing the required libraries
from flask import render_template, request, redirect, url_for, jsonify
#from app import Person
from core import Person
from core import create_person, get_all_people, get_person_by_id

def person_routes(app, db):
    
    @app.route('/person', methods=['GET', 'POST'])
    def person():
             
        person = create_person(db, firstname='Carla', lastname='Prata', age=400)
      
        all_people = get_all_people(db)
        #people = get_person_by_id(db, 1)
        return render_template('index.html', people=all_people)   
    
        #return f'Person module {all_people}'




