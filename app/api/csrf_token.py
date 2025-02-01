from flask import jsonify
from flask_restful import Resource
from app.configs_package import csrf, generate_csrf

class CSRFToken(Resource):
    def get(self):
        #token = csrf_global._get_token()
        token = generate_csrf()
        return jsonify({'csrf_token': token})


