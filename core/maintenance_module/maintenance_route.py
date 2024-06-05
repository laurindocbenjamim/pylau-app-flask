
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

def maintenance_route(app):
  
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
    
 

def remove_files_without_done():
    folder_path = 'core/static/otp_qrcode_images'
    files = os.listdir(folder_path)
        
    for file in files:
        if 'done' not in file:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
        
    return "Files without 'DONE' removed from core/static folder."


