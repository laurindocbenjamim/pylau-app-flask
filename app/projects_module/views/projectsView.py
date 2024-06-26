from flask.views import View
from flask import render_template, abort, session, redirect, url_for, request, flash,jsonify
from flask_login import login_required
from markupsafe import escape
#from flask_caching import cache

class ProjectsView(View):
    decorators = [login_required]
    """
    However, if your view class needs to do a lot of complex initialization, 
    doing it for every request is unnecessary and can be inefficient. To avoid this, set View.init_every_request to False, 
    which will only create one instance of the 
    class and use it for every request. In this case, writing to self is not safe. 
    If you need to store data during the request, use g instead.
    """
    init_every_request = True
    methods = ['GET']

    def __init__(self, userModel, userToken, template):
        self.userModel = userModel
        self.userToken = userToken
        self.template = template

    def dispatch_request(self, user_token):
        listItems = []

        if request.method == 'GET' and user_token is not None:

            status,token = self.userToken.get_token_by_token(escape(user_token))
            
            # Check if the token is expired
            if status and token is not None:
                if self.userToken.is_token_expired(token):
                    abort(401)
            else:
                abort(401)
            
             # Get the user details using the email address
            if self.userModel.check_email_exists(token.username):
                session['user_token'] = escape(user_token)
                status, users = self.userModel.get_all_users()
                if status:
                    listItems = users
                
                return render_template(self.template, user_token=token.token, title="List Users", items=listItems)
            
        return redirect(url_for('index'))