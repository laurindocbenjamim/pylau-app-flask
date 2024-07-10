
from flask.views import MethodView
from flask import json, jsonify


class ModelAPI(MethodView):
    """
    This my Model API with all methods included
    """
    init_every_request = False

    def __init__(self, model):
        self.model = model
        #self.validator = generate_validator(model)

    #
    def _get_item_by_id(self,id):
        return self.model.query.filter_by(id=id).first()
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
    
    # 
    
    
