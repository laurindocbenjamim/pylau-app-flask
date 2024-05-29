
from flask import render_template, redirect

def dev_routes(app, db):
    
    @app.route('/dev', methods=['GET'])
    def developer():
        return render_template('laurindo-c-benjamim.html')