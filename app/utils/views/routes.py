import os
import pyotp
import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape
from flask import Flask, abort, render_template, redirect,json, url_for, sessions, request, session, jsonify, make_response
from flask_cors import cross_origin
from app.auth_package.module_sign_up_sub.model.users import Users
from ...token_module import UserToken
from ...configs_package.modules.load_database import init_db_server
from flask_login import logout_user
from markupsafe import escape
#from ...utils import __get_cookies, set_header_params

def load_routes(app, db, login_manager):


    # Rate limiter to prevent abuse
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"]
    )


    # Initialize the login manager
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
       
    

    
    from .error_handlers_view import error_handlers_view
    error_handlers_view(app)
    
     # Main route
    @app.route('/')
    @app.route('/<string:user_token>')
    @limiter.limit("100 per hour", error_message='chill!')
    @cross_origin(methods=['GET'])
    def index(user_token=None):
              
        session.pop('_flashes', None)
        session['domain'] = request.root_url
        welcome_title = "Welcome to Data Tuning"
        welcome_message = "Empowering learners with cutting-edge online education"
    
        USER_DATA = {
             'USERNAME': request.cookies.get('USERNAME', ''),
        'USER_STATUS': request.cookies.get('USER_STATUS', ''),
        'USER_ROLE': request.cookies.get('USER_ROLE', ''),
        'USER_TOKEN': request.cookies.get('USER_TOKEN', '')
        }

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

        response = make_response(render_template('site_home.html', title="Home", welcome_title=welcome_title, 
                                                 welcome_message=welcome_message, 
                                                 domain = request.root_url, total_projects=12, USER_DATA=USER_DATA, user_token=user_token))
        from ..config_headers import set_header_params
        set_header_params(response)       
        response.set_cookie('current_url', request.url)
        return response
    

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


    @app.route('/about-us')
    @cross_origin(methods=['GET'])
    def about_us():
        welcome_title = "Our Courses"
        welcome_message = "Discover a world of knowledge with our diverse range of courses"
        return render_template('about.html', title="About", welcome_title=welcome_title, welcome_message=welcome_message)
    
    @app.route('/contact')
    @cross_origin(methods=['GET'])
    def contact():
        welcome_title = "Contact Us"
        welcome_message = "Discover a world of knowledge with our diverse range of courses"
        return render_template('contact.html' , title="Contact", welcome_title=welcome_title, welcome_message=welcome_message)
    
    
    
    
    @app.route('/elearning')
    @cross_origin(methods=['GET'])
    def elearning():
        return render_template('e_learning/el-base.html' , title="E-Learn")
    
    @app.route('/courses/elearning/<string:course>/<string:module>')
    @cross_origin(methods=['GET'])
    def course_elearning(course, module):
        courses=[
            {"id": 1, "course": "Python Basic","modules": ("module 1", "module 2", "module 3"), "view": "el-base.html"},
            {"id": 2, "course": "Python Intermediate","modules": ("module 1", "module 2", "module 3"), "view": "python-basic.html"},
            ]
        
        pview = next((cour['view'] for cour in courses if cour['course'] == course), None)

        if pview is not None:
            return render_template(f'e_learning/{courses[0]['view']}' , title=course)
        return render_template(f'e_learning/{courses[0]['view']}' , title="E-Learning Portal")
       
    
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
    

    from ...package_help_message.help_message_controller import HelpMessageController

    @app.route('/published/course/python-fundaments', methods=['GET', 'POST'])
    @cross_origin(methods=['GET', 'POST'])
    def python_fundamentals():   

        # Instanciation             
        help_controller = HelpMessageController()

        if request.method == 'POST':
            # Validate the form
            if help_controller.validate(request.form):
                status, data = help_controller.save(request.form)
                
                if status:
                    return jsonify({"status": status, "response": data}, 200) 
                else:
                    abort(404,description=f"Failed to send your message! {data}")
                    #return jsonify({"status": 400, "response": data}, 400)
            else:
                abort(404, description=f"Form validation failed! {data}")

        response = make_response(
        render_template(
            "marketing/python_fundamentals.html",
            title="Python Fundamentals"
            )
        )
        #set_header_params(response)
        return response
    
    @app.route('/published/course/python-fundamentals-tutorials', methods=['GET', 'POST'])
    @cross_origin(methods=['GET', 'POST'])
    def python_fundamentals_tutorials():   

        # Instanciation             
        help_controller = HelpMessageController()

        if request.method == 'POST':
            # Validate the form
            if help_controller.validate(request.form):
                status, data = help_controller.save(request.form)
                if status:
                    return jsonify({"status": 'OK', "data": data }), 200
                else:
                    abort(405,description=f"Failed to send your message! {data}")
            else:
                abort(400, description=f"Form validation failed! {data}")

        response = make_response(
        render_template(
            "marketing/python_fundamentals_tutorials.html",
            title="Python Fundamentals"
            )
        )
        #set_header_params(response)
        return response
    
       


    # Integrating the sitemap 
    from .bp_sitemap import bp_sitemap
    app.register_blueprint(bp_sitemap)

    
    # Integrating the blueprints parent and child into the application
    #"""
    from ...auth_package import bp_auth_register_parent, init_register_app
    from ...auth_package import bp_auth as bp_auth_login_view_child, init_login_app
    init_register_app()
    init_login_app(login_manager=login_manager, db=db)

    #limiter.limit("10 per minute")(bp_auth_login_view_child)
    limiter.limit("10 per minute")(bp_auth_register_parent)

    bp_auth_register_parent.register_blueprint(bp_auth_login_view_child)
    app.register_blueprint(bp_auth_register_parent)
    #"""

    
    from app.email_module import bp_email_view
    app.register_blueprint(bp_email_view)
    
    from ...package_data_science.projects_module import bp_project_view
    app.register_blueprint(bp_project_view)

    from ...admin_module.bp_admin_view import bp as bp_admin_view
    from ...package_user.bp_user import bp_user
    
    limiter.limit("50 per minute")(bp_admin_view)

    bp_admin_view.register_blueprint(bp_user)
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

    #
    from ...api.netcaixa import bp_netcaixa
    app.register_blueprint(bp_netcaixa)

    # Importing the netcaixa package
    from ...api import bp_api
    app.register_blueprint(bp_api)

    #
    from ...package_prompts.bp_prompt_ai import bp_ai
    app.register_blueprint(bp_ai)


    # Importing the reports views
    from ...package_reports import bp_reports
    app.register_blueprint(bp_reports)


    # Importing the author route 
    from ...author_profile import bp_author
    app.register_blueprint(bp_author)

    # Importing the blueprint of articles
    from ...package_blog import bp_blog
    app.register_blueprint(bp_blog)

    # Importing the blueprint of courses
    from ...package_courses import bp_courses
    

    # Importing the blueprint of my learning 
    from ...package_learning import bp_learn
    from ...package_code_editor.bp_editor_view import bp_editor

    limiter.limit("60/hour")(bp_editor)

    bp_learn.register_blueprint(bp_editor)
    bp_courses.register_blueprint(bp_learn)   
     
    app.register_blueprint(bp_courses)

    # Importing the blueprint of the audit package
    from ...package_auditapp.bp_auditapp import bp_audit
    app.register_blueprint(bp_audit)