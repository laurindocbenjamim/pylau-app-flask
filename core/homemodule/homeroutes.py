
"""
In this file, we will define the routes for our application.
"""

# Importing the required libraries
import os
import functools
from flask import render_template, g, request, redirect, url_for, jsonify, session
#from app import Person
from core import Person
from core import create_person, get_all_people, get_person_by_id

def home_routes(app, db):
    
    @app.route('/', methods=['GET'])
    def index():
        return  render_template('home2.html')
    
    @app.route('/admin', methods=['GET'])
    def adminpanel():

        all_people = get_all_people(db)
        #people = get_person_by_id(db, 1)    
        return  render_template('admin/index.html', people=all_people)
    
    @app.route('/home/public/projects', methods=['GET'])
    def public_projects():  
        token = session.get('token')
        dataframe = session.get('user_dataframe')
        return  render_template('public/projects.html', token=token, user_dataframe=dataframe)
    
    @app.route('/clean-otpimg', methods=['GET'])
    def clean_trash():
        folder_path = 'core/static/otp_qrcode_images'
        files = os.listdir(folder_path)
        removed_files = []

        for file in files:
            if 'done' not in file:
                removed_files.append(file)
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)
                
        return jsonify({'message': 'Files removed from root folder.', 'files': removed_files, 'status': 'success'}, 200)
    
    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('Auth.two_fa_app_login'))

            return view(**kwargs)

        return wrapped_view

def remove_files_without_done():
    folder_path = 'core/static/otp_qrcode_images'
    files = os.listdir(folder_path)
        
    for file in files:
        if 'done' not in file:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
        
    return "Files without 'DONE' removed from core/static folder."


