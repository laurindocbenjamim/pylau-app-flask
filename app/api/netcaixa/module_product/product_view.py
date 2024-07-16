
from flask.views import View
from flask import json, jsonify, request
from .controller import validate_words
from app import db


class ProductView(View):
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
        if request.method =='POST':
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
            
            return f'Response: {message}'
        
        if request.method =='PUT':
            if not id or id == 0 or not isinstance(id, int):
                return f"ID is required"




    
