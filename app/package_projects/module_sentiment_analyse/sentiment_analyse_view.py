
from flask.views import View
from flask import render_template, redirect, url_for, request, session, json, jsonify
from flask_login import logout_user, login_fresh, login_required
from markupsafe import escape

class SentimentAnalyseView(View):
    decorators = [login_required]
    methods = ['GET', 'POST']

    def __init__(self, userToken, template) -> None:
        super().__init__()
        self._userToken = userToken
        self._template = template

    def dispatch_request(self, user_token) -> any:
        user_token = escape(user_token)
        # Check if the token is expired
        if self.userToken.is_user_token_expired(user_token):
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))
        
        status,token = self.userToken.get_token_by_token(user_token)
        if status and token:     
            user_token = token.token       
            # Get the user details using the email address
            status, user = self.userModel.get_user_by_email(token.username)

            if request.method == 'POST':
                pass
        else:
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))

        
        return render_template(self.template, title="Sentiment Analyse", user_token=user_token)

