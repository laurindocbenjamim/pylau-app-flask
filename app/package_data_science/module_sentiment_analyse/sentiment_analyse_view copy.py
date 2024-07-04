
from flask.views import View
from flask import render_template, redirect, url_for, request, session, json, jsonify
from flask_login import logout_user, login_fresh, login_required
from markupsafe import escape

class SentimentAnalyseView(View):
    #decorators = [login_required]
    methods = ['GET', 'POST']

    def __init__(self, userToken, userModel, template) -> None:
        super().__init__()
        self._userToken = userToken
        self._userModel = userModel
        self._template = template

    def dispatch_request(self, user_token) -> any:
        
        user_token = escape(user_token)
        status = 200
        message = 'Teste'
        category = 'info'

        #if user_token == '401': return redirect(url_for('auth.user.login'))
        # Check if the token is expired
        """if self._userToken.is_user_token_expired(user_token):
            session.clear()
            logout_user()
            session['current_route'] = 'data_science.project.sentiment_analyse' 
            #return redirect(url_for('auth.user.login'))
        
        status,token = self._userToken.get_token_by_token(user_token)
        if status and token:     
            user_token = token.token       
            # Get the user details using the email address
            status, user = self._userModel.get_user_by_email(token.username)

            if request.method == 'POST':
                pass
        else:
            session.clear()
            logout_user()
            return redirect(url_for('auth.user.login'))
        """
        if request.method =='POST':
            comment = request.form.get('comment', None)
            if comment is None or comment == '':
                status = 400
                message = 'Enter a comment to analyse'
                category = 'error'
            else:
                status = 200
                message = f'COMMENT RECEIVED: {comment}'
                category = 'info'

            return jsonify({"message": message, "category": category},status)

        
        return render_template(self._template, title="Sentiment Analyse", user_token=user_token)

