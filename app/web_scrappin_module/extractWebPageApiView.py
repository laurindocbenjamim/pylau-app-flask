
from flask import session, render_template, url_for, redirect, request, jsonify
from markupsafe import escape
from flask_login import logout_user
from flask.views import View

class ExtractWebPageApiView(View):
    methods = ['POST']

    def __init__(self,userModel, userToken, template):
        self.userModel = userModel
        self.userToken = userToken
        self.template = template

    def dispatch_request(self):
        status = 200
        message = '?'
        category = '?'
        obj = []
        user_token = session['user_token'] if 'user_token' in session and session['user_token'] is not None else ''

        if self.userToken.is_user_token_expired(escape(user_token)):
            session.clear()
            logout_user()
            return jsonify({"message": 'Session expired', "category": 'danger', "object":obj},401)

        
        if request.method == 'GET' and user_token is not None:

            status,token = self.userToken.get_token_by_token(escape(user_token))
            
             # Get the user details using the email address
            if status and self.userModel.check_email_exists(token.username):
                session['user_token'] = token.token               
                message = 'The page is ready'
                category = 'info'
                status = 200
        elif request.method == 'POST':
            url = request.form.get('url', None) 

            if url is None or url == '':
                message = 'URL is required'
                category = 'error'
                status = 400
            else:
                message = url
                category = 'success'
                status = 200
            
        return jsonify({"message": message, "category": category, "object":obj},status)
