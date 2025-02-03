
import os
from app.dependencies import secrets
from app.dependencies import pyotp
from app.dependencies import escape
from app.dependencies import render_template
from app.dependencies import redirect
from app.dependencies import abort
from app.dependencies import url_for
from app.dependencies import request
from app.dependencies import session
from app.dependencies import jsonify
from app.dependencies import make_response
from app.dependencies import cross_origin, send_file
from app.configs_package import csrf, generate_csrf

from app.utils.config_headers import set_header_params

# Importing the login manager
from app.auth_package.module_sign_up_sub.model.users import Users

from app.configs_package.modules.load_database import init_db_server
from app.utils.my_file_factory import save_uploaded_file, generate_strong_secret_key, remove_edit_protection, remove_pdf_protection


root_files_path='static'

def load_routes(app, db, login_manager, limiter):

    # Initialize the login manager
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
     
    
    """from app.utils.views.error_handlers_view import error_handlers_view
    error_handlers_view(app)"""
    
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

    from app.utils.executesql import execute_sql

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
    

    from app.package_help_message.help_message_controller import HelpMessageController

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
    
    from app.api.storage.repository import upload_file, upload_file_object

    @app.route('/videos/post', methods=['GET','POST'])
    @cross_origin(methods=['GET','POST'])
    @csrf.exempt
    def video_post():
       # Check if the request contains the file part
        if 'videoFileToAnalyze' not in request.files:
            return jsonify({"status":400, "error": "No video file to analyze has been found!"})

        file = request.files['videoFileToAnalyze']
        
        # Check if a file has been selected
        if file.filename == '':
            return jsonify({"status":400, "error": "No selected file"})

        # Use the save_uploaded_file function from the module
        file_directory=os.path.join(app.root_path, root_files_path, app.config['UPLOAD_FOLDER'], app.config['UPLOAD_VIDEO_FOLDER'])
        #status,result = save_uploaded_file(file, file_directory)
        status, result = upload_file(file=file)
        if not status:
            return jsonify(result)
        return jsonify(result)


    #
    @app.route('/pdf-unlock/remove-protecction', methods=['POST'])
    @cross_origin(methods=['POST'])
    @csrf.exempt
    def pdf_pdf_protection():

        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        password = request.form.get('password', '')

        if file.filename == '':
            return "No selected file", 400

        filepath = os.path.join(app.root_path, root_files_path, app.config['UPLOAD_FOLDER'], app.config['UPLOAD_DOCS_FOLDER'], file.filename)
        file.save(filepath)

        try: #app.root_path, root_files_path, app.config['MODIFIED_FOLDER']
            # Attempt to remove protection
            decrypted_file = os.path.join(app.root_path, root_files_path, app.config['UPLOAD_FOLDER'], app.config['DECRYPTED_FOLDER'], f"decrypted_{file.filename}")
            remove_pdf_protection(filepath, decrypted_file, password)
            return send_file(decrypted_file, as_attachment=True)
        except Exception as e:
            return f"Error: {e}", 500
        finally:
            # Cleanup
            if os.path.exists(filepath):
                os.remove(filepath)

    @app.route('/pdf-unlock/modify-permition', methods=['POST'])
    @cross_origin(methods=['POST'])
    @csrf.exempt
    def pdf_modify_permitions():
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        # Get the file size
        file_size = file.content_length / (1024 * 1024)  # Size in MB
        if file_size > 20:
            return f"File size must be less or equals 20MB. (Your file have {file_size}MB)"
        #app.root_path, 'static', app.config['MODIFIED_FOLDER']
        filepath = os.path.join(app.root_path, root_files_path, app.config['UPLOAD_FOLDER'], app.config['UPLOAD_DOCS_FOLDER'], file.filename)
        file.save(filepath)

        try:
            # Process the file to remove edit protection
            modified_file = os.path.join(app.root_path, root_files_path, app.config['UPLOAD_FOLDER'], app.config['MODIFIED_FOLDER'], f"unrestricted_{file.filename}")
            remove_edit_protection(filepath, modified_file)
            # Send the file as a binary download
            return send_file(modified_file, as_attachment=True, download_name=f"unrestricted_{file.filename}")
        except Exception as e:
            return f"Error: {e}", 500
        finally:
            # Cleanup
            if os.path.exists(filepath):
                os.remove(filepath)

    @app.route('/secrete-key')
    def sercrete_key():
        
        return f"Secrete-key: {generate_strong_secret_key()}"

