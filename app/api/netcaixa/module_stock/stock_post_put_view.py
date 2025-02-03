

from datetime import datetime
from flask.views import View
from flask import json, jsonify, request
from .controller import validate_words
from app.configs_package.modules.load_database import db


class StockPostPutView(View):
    """
 
    """
    methods = ['POST', 'PUT']

    def __init__(self, model, template):
        self.model = model
        self.template = template
        
    def dispatch_request(self, product_barcode = None):

        
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
                message = "The product has been stocked successfully."
                category = "success"  
                code == 200  
                prod_status = True
                if 'False' or 'false' or 0 or '0' in request.form.get('status', True):
                    prod_status = False
                data = {
                    "product_barcode": request.form.get('product_barcode', None),
                    "product_description": request.form.get("product_description",None),
                    "product_unitary_price": request.form.get("product_unitary_price",None),
                    "product_iva": request.form.get("product_iva",None),
                    "product_iva_code": request.form.get("product_iva_code",None),
                    "product_profit": request.form.get("product_profit",None),
                    "product_quantity": request.form.get("product_quantity",None),
                    "stock_pos": request.form.get("stock_pos",None),
                    "stock_location": request.form.get("stock_location",None),
                    "stock_code": request.form.get("stock_code",None),
                    "stock_date_added": request.form.get("stock_date_added",None),
                    "stock_year_added": request.form.get("stock_year_added",None),
                    "stock_month_added": request.form.get("stock_month_added",None),
                    "stock_datetime_added": request.form.get("stock_datetime_added",None),
                    "stock_date_updated": request.form.get("stock_date_updated",'null')
                }
                status, obj = self.model.create(data)
                if not status:
                    message = f"Failed to create stock. \nError: [{obj}]"
            
            return f'{message}'
        
        if request.method =='PUT':
            
            if product_barcode is not None and isinstance(product_barcode, str):
                
                # Filter and validate each of the form field
                for key, value in request.form.items():
                    status, sms = validate_words(key=key, value=value)
                    if not status:
                        message = f'{sms}'
                        category = "error"
                        code = 400
                        break
                
                if code == 200:   
                    message = "The stock has been updated successfully."
                    category = "success"  
                    code == 200  
                    prod_status = True
                    if 'False' or 'false' or 0 or '0' in request.form.get('status', True):
                        prod_status = False
                    data = {
                    "product_barcode": request.form.get('product_barcode', None),
                    "product_description": request.form.get("product_description",None),
                    "product_unitary_price": request.form.get("product_unitary_price",None),
                    "product_iva": request.form.get("product_iva",None),
                    "product_iva_code": request.form.get("product_iva_code",None),
                    "product_profit": request.form.get("product_profit",None),
                    "product_quantity": request.form.get("product_quantity",None),
                    "stock_pos": request.form.get("stock_pos",None),
                    "stock_location": request.form.get("stock_location",None),
                    "stock_code": request.form.get("stock_code",None),
                    "stock_date_added": request.form.get("stock_date_added",None),
                    "stock_year_added": request.form.get("stock_year_added",None),
                    "stock_month_added": request.form.get("stock_month_added",None),
                    "stock_datetime_added": request.form.get("stock_datetime_added",None),
                    "stock_date_updated": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                }
                    
                    status, obj = self.model.update(product_barcode, data)
                if not status:
                    message = f"Failed to create stock. \nError: [{obj}]"
            
            return f'{message}'




    
