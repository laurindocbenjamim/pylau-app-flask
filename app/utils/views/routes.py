import os
import pyotp
import secrets
from flask import Flask, abort, render_template, redirect,json, url_for, sessions, request, session, jsonify
from flask_cors import cross_origin
from app.auth_package.module_sign_up_sub.model.users import Users
from ...token_module import UserToken
from ...configs_package.modules.load_database import init_db_server
from flask_login import logout_user
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

    from ...utils import execute_sql
    @app.route('/exec-sql')
    @cross_origin(methods=['GET'])
    def execute_raw_sql():       
        
        sql = "CREATE TABLE your_table_name (\
                subscriber_id INT PRIMARY KEY,\
                email VARCHAR(100) NOT NULL,\
                is_active BOOLEAN DEFAULT TRUE,\
                year_added CHAR(5) DEFAULT EXTRACT(YEAR FROM CURRENT_TIMESTAMP),\
                month_added CHAR(10) DEFAULT EXTRACT(MONTH FROM CURRENT_TIMESTAMP),\
                date_added DATE DEFAULT CURRENT_DATE,\
                datetime_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
            )"
        sql_pgs = "CREATE TABLE subscribers (\
            subscriber_id SERIAL PRIMARY KEY,\
            email VARCHAR(100) NOT NULL,\
            is_active BOOLEAN DEFAULT TRUE,\
            year_added CHAR(5) DEFAULT TO_CHAR(CURRENT_TIMESTAMP, 'YYYY'),\
            month_added CHAR(10) DEFAULT TO_CHAR(CURRENT_TIMESTAMP, 'MM'),\
            date_added DATE DEFAULT CURRENT_DATE,\
            datetime_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
        )"
        status, response = execute_sql(sql_pgs)
        response = "SQL Executed successfully" if status else response
        #return redirect(url_for('index'))
        return jsonify({"status": status, "response": response})
    
    @app.route('/create-db')
    @cross_origin(methods=['GET'])
    def create_db():       
        init_db_server(app=app)

        return redirect(url_for('index'))

    @app.route('/app-logs')
    @cross_origin(methods=['GET'])
    def display_logs():

        if 'user_token' in session:
            user_token = session['user_token']
            if len(escape(user_token)) < 100 or len(escape(user_token)) > 200:
                session.clear()
                logout_user()
                return redirect(url_for('auth.user.login'))            
            
            if UserToken.is_user_token_expired(user_token):
                session.clear()
                logout_user()
                return redirect(url_for('auth.user.login'))
        
            if request.method == 'GET' and user_token is not None:

                status,token = UserToken.get_token_by_token(user_token)
                
                # Get the user details using the email address
                if status and Users.check_email_exists(token.username):
                    session['user_token'] = token.token          

        #return jsonify({"user": session['user_token']})
        logs = "app/static/logs/logs.log"
        log_data =''
        with open(logs, 'r') as data:
            log_data = data.read()
        return render_template('home.html', title='Display Logs', log_data=log_data)
    

     # Main route
    @app.route('/')
    @app.route('/<string:user_token>')
    @cross_origin(methods=['GET'])
    def index(user_token=None):
        
        session.pop('_flashes', None)

        if user_token is not None:
            if len(escape(user_token)) < 100 or len(escape(user_token)) > 200:
                abort(401)
            token = escape(user_token)
            session['user_token'] = escape(user_token) if 'user_id' in session else None 
            
            if user_token == 'favicon.ico': 
                session.pop('user_token', None)
                user_token = ''
        elif 'user_token' in session:
            user_token = session.pop('user_token', None) if session['user_token'] == 'favicon.ico' else session['user_token']
        #return jsonify({'status': 'success', 'message': 'Welcome to the home page', 'user_token': user_token})
        return render_template('site_home.html', total_projects=12, user_token=user_token)
    
       
    
    @app.route('/get-secret', methods=['GET'])
    @cross_origin(methods=['GET'])
    def get_secret():                

        #session['user_token'] = ''
        t_key = secrets.token_urlsafe(32)
        otp_secret = pyotp.random_base32()
            
        return jsonify({
            'token_secret': t_key, 
            'otp_secret': otp_secret
            })
    
       

    from .error_handlers_view import error_handlers_view
    error_handlers_view(app)

    
    # Integrating the blueprints parent and child into the application
    from ...auth_package import bp_auth_register_parent, init_register_app
    from ...auth_package import bp_auth as bp_auth_login_view_child, init_login_app
    init_register_app()
    init_login_app(login_manager=login_manager, db=db)
    bp_auth_register_parent.register_blueprint(bp_auth_login_view_child)
    app.register_blueprint(bp_auth_register_parent)

    
    from app.email_module import bp_email_view
    app.register_blueprint(bp_email_view)
    
    from ...package_data_science.projects_module import bp_project_view
    app.register_blueprint(bp_project_view)

    from ...admin_module.bp_admin_view import bp as bp_admin_view
    app.register_blueprint(bp_admin_view)

    from ...test_forms.bp_form import bp as bp_form
    app.register_blueprint(bp_form)

    from ...web_scrappin_module.bp_web_scrapping_view import bp as bp_web_scrapping_view
    app.register_blueprint(bp_web_scrapping_view)

    from ...subscription_module import bp as bp_subscriber
    app.register_blueprint(bp_subscriber)

    #from ...package_data_science.bp_data_science_view import bp_data_science
    from ...package_data_science import bp_data_science
    app.register_blueprint(bp_data_science)


    # Importing the netcaixa package
    from ...api import bp_api
    app.register_blueprint(bp_api)

    #
    from ...package_prompts.bp_prompt_ai import bp_ai
    app.register_blueprint(bp_ai)