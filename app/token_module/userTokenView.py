
from flask.views import View
from flask import request, jsonify, current_app, render_template, redirect, url_for, flash

class UserTokenView(View):
    
    def __repr__(self) -> str:
        return '<UserTokenView %r>' % self.username
    
    def __init__(self, model) -> None:        
        self.model = model

    def dispatch_request(self):
        if request.method == 'POST':
            return self.create_token()
        return 'UserTokenView'