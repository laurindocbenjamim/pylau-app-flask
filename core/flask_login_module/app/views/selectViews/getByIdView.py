
from flask.views import View
from flask import render_template, redirect, url_for, request, flash, session, jsonify

class GetByIdView(View):
    """
    However, if your view class needs to do a lot of complex initialization, 
    doing it for every request is unnecessary and can be inefficient. To avoid this, set View.init_every_request to False, 
    which will only create one instance of the 
    class and use it for every request. In this case, writing to self is not safe. 
    If you need to store data during the request, use g instead.
    """
    init_every_request = True
    methods = ['GET']

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self, id):
        #item = self.model.query.get_or_404(id)
        item = self.model.get_item_by_id(id)
        return render_template(self.template, item=item)