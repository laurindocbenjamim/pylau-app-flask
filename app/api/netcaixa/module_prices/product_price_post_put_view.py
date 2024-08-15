

from flask.views import View
from flask import request, jsonify, render_template, redirect
from .controller import validate_words

class ProductPricePostPutViev(View):
    """
    This class  is used to create the price View 
    """
    methods = ['POST', 'PUT']

    def __init__(self, price, template) -> None:
        super().__init__()
        self._price = price
        self._template = template

    
    def dispatch_request(self):

        message = ""
        error = ""
        category = ""
        status = False

        if request.method == 'POST':
            for key, value in request.form.items():
                status, sms = validate_words(key=key, value=value)
                if not status:
                    message = f'{sms}'
                    category = "error"
                    break
            
            if status:
                return f"ready to save {status}"
            return f"{message}"
        elif request.method == 'PUT':
            return f"ready to update"
        else:
            return f"Method not allowed!"