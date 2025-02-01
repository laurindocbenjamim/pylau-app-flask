
from flask import session, render_template, url_for, redirect, request
from markupsafe import escape
from flask_login import logout_user
from flask.views import View

class ExtractWebPageView(View):
    methods = ['GET', 'POST']

    def __init__(self,userModel, userToken, template):
        self.userModel = userModel
        self.userToken = userToken
        self.template = template

    def dispatch_request(self, user_token):

        if self.userToken.is_user_token_expired(escape(user_token)):
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))
        
        if request.method == 'GET' and user_token is not None:

            status,token = self.userToken.get_token_by_token(escape(user_token))
            
             # Get the user details using the email address
            if status and self.userModel.check_email_exists(token.username):
                session['user_token'] = token.token               
                
                return render_template(self.template, title="ETL-Webscraping", user_token=token.token)
            
        return redirect(url_for('index'))
