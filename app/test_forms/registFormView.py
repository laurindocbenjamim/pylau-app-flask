from flask import render_template, redirect, request
from flask.views import MethodView
from .registForm import RegistForm

class RegistFormView(MethodView):



    def __init__(self, template) -> None:
        self.template = template

    def dispatch_request(self):
        form = RegistForm(request.form)

        if request.method == 'POST' and form.validate():
            # Save form data to the database
            return {'message': 'Form submitted successfully!'}

        return render_template(self.template, form=form)