from flask.views import View
from flask import render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_required
from ...controller.validate_user_form import validate_user_form

class CreateView(View):
    methods = ['GET', 'POST']
    """
    However, if your view class needs to do a lot of complex initialization, 
    doing it for every request is unnecessary and can be inefficient. To avoid this, set View.init_every_request to False, 
    which will only create one instance of the 
    class and use it for every request. In this case, writing to self is not safe. 
    If you need to store data during the request, use g instead.
    """
    init_every_request = False

    def __init__(self, model, template):
        self.model = model
        self.template = template
        #self.form = form
    
    def dispatch_request(self):
        #form = self.form(request.form)
        #if request.method == 'POST' and form.validate():
        if request.method == 'POST':
            if validate_user_form(request.form):
                username = request.form.get('username')
                #self.model.create_user(form)
                flash('User created successfully', 'success')
                #return redirect(url_for('create'))
                #return jsonify({'message':'User created successfully!!!', 'username':username})
        return render_template(self.template, title='Create User')
        #return jsonify({'message':'User not created!!!!!'})