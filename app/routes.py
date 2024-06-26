import os
import pyotp
import secrets
from flask import Flask, abort, render_template, redirect, url_for, sessions, request, session, jsonify
from flask_cors import cross_origin
from .user_module.model.users import Users
from markupsafe import escape

def load_routes(app, db, login_manager):
    # Initialize the login manager

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
       
    
    """
    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('username')
        
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.is_active() == True:
                # Use the login_user method to log in the user  
                if 'user_token' in session:
                    return redirect(url_for('index', user_token=session['user_token']))   
        return 
    """

    @app.route('/create-db')
    def create_db():
        with app.app_context():
            db.create_all()
        return redirect(url_for('index'))
    

     # Main route
    @app.route('/')
    @app.route('/<string:user_token>')
    @cross_origin(methods=['GET'])
    def index(user_token=None):
        if user_token is not None:
            if len(escape(user_token)) < 100 or len(escape(user_token)) > 200:
                abort(401)

            session['user_token'] = [escape(user_token) if 'user_id' in session else None ]
            
            if user_token == 'favicon.ico': 
                session.pop('user_token', None)
                user_token = ''
        elif 'user_token' in session:
            user_token = [session.pop('user_token', None) if session['user_token'] == 'favicon.ico' else session['user_token']]
        #return jsonify({'status': 'success', 'message': 'Welcome to the home page', 'user_token': user_token})
        return render_template('site_home.html', user_token=user_token)
    
    from .views.error_handlers_view import error_handlers_view
    error_handlers_view(app)
    
    
    @app.route('/get-secret', methods=['GET'])
    @cross_origin(methods=['GET'])
    def get_secret():                

        #session['user_token'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoicm9ja2V0bWMyMDA5QGdtYWlsLmNvbSIsImV4cCI6MTcxOTMxNDU0NiwibmJmIjoxNzE5MzEyNzQ2fQ.sBMAHsZ7IpH7TFbGwHmLbYCUYAGZ0bKQ0t7-nXOQnFc'
        t_key = secrets.token_urlsafe(32)
        otp_secret = pyotp.random_base32()
            
        return jsonify({
            'token_secret': t_key, 
            'otp_secret': otp_secret
            })
    
    # Integrating the blueprints parent and child into the application

    from .auth_login_module import init_auth_login_view_app, bp_auth_login_view_child
    from .user_module import bp_auth_register_parent, init_user_register_app
    
    init_user_register_app()
    init_auth_login_view_app(login_manager=login_manager, db=db)
    bp_auth_register_parent.register_blueprint(bp_auth_login_view_child)
    app.register_blueprint(bp_auth_register_parent)

    from .send_email_module.bp_send_email_view import bp as bp_send_email_view
    app.register_blueprint(bp_send_email_view)
    
    from .projects_module import bp_project_view
    app.register_blueprint(bp_project_view)

    from .adminmodule.bp_admin_view import bp as bp_admin_view
    app.register_blueprint(bp_admin_view)

    from .test_forms.bp_form import bp as bp_form
    app.register_blueprint(bp_form)

    from .web_scrappin_module.bp_web_scrapping_view import bp as bp_web_scrapping_view
    app.register_blueprint(bp_web_scrapping_view)