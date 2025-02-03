
from flask.views import View
from flask import json, jsonify, request
from .controller import validate_words
from app.configs_package.modules.load_database import db


class DeleteProductView(View):
    """
    This class is specific to delete product from 
    database
    """
    methods = ['GET']

    def __init__(self, model, template):
        self.model = model
        self.template = template
        
    def dispatch_request(self, id):
        """
        """
        message = ''
        obj = []
        category = ''
        code = 200
        
        if request.method =='GET':
            if id is not None and isinstance(id, int):
                status, obj = self.model.delete_product(id)
                return jsonify({"status": status, "category": "success"}, code)
        return jsonify({"message":"Failed to delete product", "category": "error"},400)