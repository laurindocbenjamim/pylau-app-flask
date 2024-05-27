
import os
from flask import (
    Flask, jsonify, render_template, url_for, request, json
)
from flask_cors import CORS

def create_application(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    app.config.from_mapping(
        SECRET_KEY="AB8D23A974B4C7B2ABB641668F9F9",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    from . modules.codeskill import dictionaries
    app.register_blueprint(dictionaries.bpapp)

    from . modules.authmodule import auth
    app.register_blueprint(auth.bpapp)

    from . modules.authmodule import two_factor_auth
    app.register_blueprint(two_factor_auth.bpapp)

    #from . modules.smtp import sendemail

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'rocketmc2009@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jgtkeopkbwoxkjoo'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    #sendemail.mail.init_app(app)
    #app.register_blueprint(sendemail.bpapp)

    from . modules.authmodule import two_factor_google_auth
    app.register_blueprint(two_factor_google_auth.bpapp)



    #from . modules.authmodule import authapi
    #from . modules.authmodule import register


    @app.route('/api', methods=['GET', 'POST'])
    def api():
        return render_template('fetchapi/api.html')

    @app.route('/', methods=['GET'])
    def index():
        return  render_template('home2.html')

    @app.route('/home', methods=['GET'])
    def home():
        return render_template('laurindo-c-benjamim.html')

    @app.route('/person', methods=['GET', 'POST'])
    def person():
        peoples=[]
        
        if request.method =='GET':            
            return jsonify({"object": peoples})
        if request.method == 'POST':
            code = request.form['code']
            peoples.append({"name": "new", "age": code})
            return jsonify({"object": peoples})
    
    @app.route('/laurindo', methods=['GET'])
    def blog():
        return jsonify({"msms": 1222})

    return app

