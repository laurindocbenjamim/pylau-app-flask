
from datetime import datetime
from flask.views import View
from flask import json, jsonify, request
from .controller import validate_words
from app import db


class ProductView(View):
    """
 
    """
    methods = ['GET', 'POST', 'PUT']

    def __init__(self, model, template):
        self.model = model
        self.template = template
        
    def dispatch_request(self, id = None, barcode=None):

        

        def get_all_products()->any:
            if not id or id is None:                
                status, obj = self.model.get_all()
                if status:
                    products = self.model.convert_to_list(obj)                            
                    return jsonify({"status":status, "object": len(products)}, 200)
            return {"message":"List of products", "category": "error", "object": []}, 400

        # Method to get product by ID
        def get_product_by_id(id)->any:
            if isinstance(id, int):                
                status, obj = self.model.get_by_id(id)
                if status:
                    return f"ID {id}"
                    #product = self.model.convert_to_list(obj)
                    return jsonify({"status":status, "object": obj }, 200) 
            return jsonify({"message":"List of products", "category": "error", "object": []}, 400)

        # Method to get products by barcode
        def get_product_by_barcode(barcode)->any:
            if isinstance(barcode, str):
                status, obj = self.model.get_by_barcode(barcode)
                if status:
                    return f"BARCODE {barcode}"
                    return jsonify({"status":status, "object": len(self.model.convert_to_list(obj)) }, 200) 
            return jsonify({"message":"List of products", "category": "error", "object": []}, 400)

        # Method to get product by description
        def get_product_by_description(description:str)->self.model:
            if isinstance(barcode, str):
                status, obj = self.model.get_by_description(description)
                if status:
                    return jsonify({"status":status, "object": self.model.convert_to_list(obj) }, 200) 
            return jsonify({"message":"List of products", "category": "error", "object": []}, 400)
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
                return get_all_products()
                #status, obj = self.model.get_all()
                #return jsonify({"message":"List of products", "category": "success", 
                                #"object": len(obj) if status else []},code)
            elif id is not None:
                return get_product_by_id(id)
            elif barcode is not None:
                obj, code = get_product_by_barcode(barcode=barcode)
                return jsonify(obj, code)
            return jsonify({"message":"List of products", "category": "error", "object": []}, 400) 
        
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
                message = "The product has been created successfully."
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
                if not status:
                    message = f"Failed to create product. Error: [{obj}]"
            
            return f'{message}'
        
        if request.method =='PUT':
            if id is not None and isinstance(id, int):
                # Filter and validate each of the form field
                for key, value in request.form.items():
                    status, sms = validate_words(key=key, value=value)
                    if not status:
                        message = f'{sms}'
                        category = "error"
                        code = 400
                        break

                if code == 200:   
                    message = "The product has been updated successfully."
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
                        'product_date_updated': datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    }
                    status, obj = self.model.update_(id, data)
                if not status:
                    message = f"Failed to update the product. Error: [{obj}]"
            
            return f'{message}'




    
