
from flask.views import View
from flask import json, jsonify, request
from .controller import validate_words
from app import db


class StockDeleteProductView(View):
    """
    This class is specific to delete product from 
    database
    """
    methods = ['GET']

    def __init__(self, model, template):
        self.model = model
        self.template = template
        
    def dispatch_request(self, item):
        """
        """
        message = ''
        obj = []
        category = ''
        code = 200
        authorized_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        if request.method =='GET':
            if item is None:
                return f"Not founded"
            elif not isinstance(item, str):
                return f"Invalid type value"
            elif any(char not in authorized_chars for char in item):
                return f"Invalid charcteres detected!"
            elif len(item) > 10:
                return f"Invalid size value"
            else:                
                status, obj = self.model.delete_product(item)
                if status:
                    return f"The item {item} has been removed successfully."
                #return jsonify({"status": status, "category": "success"}, code)
        #return jsonify({"message":"Failed to delete product", "category": "error"},400)
        return f"Failed to remove element.{item}"