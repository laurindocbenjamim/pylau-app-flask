
from flask.views import MethodView
from flask import json, jsonify, request
from .controller import validate_words
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
        return {"GET": f'Your ID {id}'}
        
    #
    #def get(self,with_param=False, **kwargs)->any:
    def get(self,id=None)->any:
        """
        This is the method to get the product from the database

        Parameters:
            By default the method use kwargs meant that can receive many arguments
            but the method itselve expect arguments related by the class object
        
        id = kwargs.get('product_id', None)
        barcode = kwargs.get('product_barcode', None)
        response = []
        """
        if not id:
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
        message = ''
        obj = []
        category = ''
        code = 200
        
        # Filter and validate each of the form field
        for key, value in request.form.items():
            status, sms = validate_words(key=key, value=value)
            if not status:
                message = f'{sms}'
                category = "error"
                code = 400
                break

        if code == 200:   
            message = "Test passed"
            category = "success"  
            code == 200  
            prod_status = True
            if 'False' or 'false' or 0 or '0' in request.form.get('status', True):
                prod_status = False
            data = {
                'barcode':  request.form.get('barcode', None),
                'description': request.form.get('description', None),
                'category': request.form.get('category', None),
                'type': request.form.get('type', None),   
                'detail': request.form.get('detail', None),
                'brand': request.form.get('brand', None),
                'measure_unit': request.form.get('measure_unit', None),
                'fixed_margin': request.form.get('fixed_margin', None),
                'status': prod_status,
                'retention_font': request.form.get('retention_font', None),
                'date_added': request.form.get('date_added', None),
                'year_added': request.form.get('year_added', None),
                'month_added': request.form.get('month_added', None),
                'datetime_added': request.form.get('datetime_added', None),
            }
            status, obj = self.model.create_product(data)
            message = status
        #return jsonify({"message":message, "category": category, "object": len(obj)},code)
        return f'Response: {message}'


    
