
from flask.views import MethodView
from flask import json, jsonify, request
from .controller import validate_field
from app import db


class ProductAPI(MethodView):
    """
    This my Product API with all methods included
    """
    init_every_request = True

    def __init__(self, model):
        self.model = model
        #self.validator = generate_validator(model)

    #
    def _get_item_by_id(self,id):
        return self.model.get_by_id(id)
        
    #
    def get(self,with_param=False, **kwargs)->any:
        """
        This is the method to get the product from the database

        Parameters:
            By default the method use kwargs meant that can receive many arguments
            but the method itselve expect arguments related by the class object
        """
        id = kwargs.get('product_id', None)
        barcode = kwargs.get('product_barcode', None)
        response = []
        if not with_param:
            response = self.model.get_all_()
        else:
            response = self._get_item_by_id(id=id)
        return jsonify(response)
    
    def patch(self, id):
        item = self._get_item(id)
        errors = self.validator.validate(item, request.json)

        if errors:
            return jsonify(errors), 400

        item.update_from_json(request.json)
        db.session.commit()
        return jsonify(item.to_json())

    def delete(self, id):
        item = self._get_item(id)
        db.session.delete(item)
        db.session.commit()
        return "", 204
    
    # 
    def post(self):
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
        message = ""
        obj = []
        category = ''
        if not validate_field(request.form.get('description')):            
            return jsonify({"message":message, "category": category, "object": obj},400)
        else:
            obj.append(
                {"id": 1, "barcode": request.form.get('barcode'),
                 "description": request.form.get('description')
                 })
            return jsonify({"message":message, "category": category, "object": obj},200)


    
