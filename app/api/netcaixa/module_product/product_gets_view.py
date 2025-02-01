
from flask.views import View
from flask import json, jsonify, request
from .controller import validate_words
from app import db


class ProductGetsView(View):
    """
 
    """
    methods = ['GET', 'POST']

    def __init__(self, model, template):
        self.model = model
        self.template = template
        
    def dispatch_request(self, id = None):
        """
        
        """
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
                    return jsonify({"status":status, "object": obj.product_id }, 200) 
            return jsonify({"message":"List of products", "category": "error", "object": []}, 400)

        # Method to get products by barcode
        def get_product_by_barcode(barcode)->any:
            if isinstance(barcode, str):
                status, obj = self.model.get_by_barcode(barcode)
                if status:
                    return jsonify({"status":status, "object": obj.product_barcode }, 200) 
            return jsonify({"category": barcode}, 400)

        # Method to get product by description
        def get_product_by_description(description:str)->self.model:            
            if isinstance(description, str):
                status, obj = self.model.get_by_description(description)
                if status:
                    return jsonify({"status":status, "object": obj.product_description }, 200) 
            return jsonify({"message":"List of products", "category": "error", "object": []}, 400)
       
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
                message = "Test passed"
                category = "success"  
                code == 200  
                prod_status = True
                barcode = request.form.get('barcode', None)
                description = request.form.get('description', None)

                if barcode is not None:
                    return get_product_by_barcode(barcode)
                elif description is not None:
                    return get_product_by_description(description)
            
            return f"ID is required. IDs {id} -- {message}"




    
