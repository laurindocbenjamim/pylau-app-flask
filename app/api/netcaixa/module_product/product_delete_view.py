
from flask.views import View
from flask import json, jsonify, request
from .controller import validate_words
from app import db


class DeleteProductView(View):
    """
 
    """
    methods = ['GET', 'POST']

    def __init__(self, model, template):
        self.model = model
        self.template = template
        
    def dispatch_request(self, id=None):
        """
        errors = self.validator.validate(request.json)

        if errors:
            return jsonify(errors), 400

        db.session.add(self.model.from_json(request.json))
        db.session.commit()
        return jsonify(item.to_json())
        obj = self.model._get_object()
        resp = self.model.create_product(obj)
        return True, resp
        """
        message = ''
        obj = []
        category = ''
        code = 200
        
        if request.method =='GET':
            if not id or id is None:
                status, obj = self.model.get_all()
                return jsonify({"message":"List of products", "category": "success", "object": len(obj)},code)
            elif id is not None and isinstance(id, int):
                status, obj = self.model.get_by_id(id)
                #return jsonify({"message":f"Product selected-{id}", "category": "success", "object": len(obj)},code)
                return f"ID: {obj.product_id}"
        return jsonify({"message":f"Product selected-{id}", "category": "success", "object": len(obj)},code)