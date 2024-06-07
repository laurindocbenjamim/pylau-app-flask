from flask.views import View
from flask import render_template, redirect, url_for, request, flash, session, jsonify
#from flask_login import login_required
#from flask_caching import cache

class ListView(View):
    #decorators = [cache(minutes=2), login_required]
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

    def dispatch_request(self):
        listItems = self.model.list_users()
        return render_template(self.template, title="List Users", items=listItems)