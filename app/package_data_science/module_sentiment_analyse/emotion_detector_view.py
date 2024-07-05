
from flask.views import View
from flask import render_template, redirect, url_for, request, session, json, jsonify
from flask_login import logout_user, login_fresh, login_required
from markupsafe import escape

class EmotionDetectorView(View):
    #decorators = [login_required]
    methods = ['GET', 'POST']

    def __init__(self, userToken, userModel, EmotionDetector, template) -> None:
        super().__init__()
        self._userToken = userToken
        self._userModel = userModel
        self._emotionDetector = EmotionDetector
        self._template = template

    def dispatch_request(self, user_token) -> any:
        
        user_token = escape(user_token)
        status = 200
        message = 'Teste'
        category = 'info'
        emotions = []

        if user_token == '401': return redirect(url_for('auth.user.login'))
        # Check if the token is expired
        if self._userToken.is_user_token_expired(user_token):
            session.clear()
            logout_user()
            session['current_route'] = 'data_science.project.emotion_detector' 
            return redirect(url_for('auth.user.login'))
        
        status,token = self._userToken.get_token_by_token(user_token)
        if status == False:            
                session.clear()
                logout_user()
                session['current_route'] = 'data_science.project.emotion_detector' 
                return redirect(url_for('auth.user.login'))
        if not token:
            session.clear()
            logout_user()
            session['current_route'] = 'data_science.project.emotion_detector' 
            return redirect(url_for('auth.user.login'))
        else:     
            user_token = token.token       
            # Get the user details using the email address
            status, user = self._userModel.get_user_by_email(token.username)

            if status == False:            
                session.clear()
                logout_user()
                session['current_route'] = 'data_science.project.emotion_detector' 
                return redirect(url_for('auth.user.login'))
            else:       
                if request.method =='POST':

                    if user_token == '401': return jsonify({"message": 'Session expired', "category": 'danger', 'emotions': [],
                                                            'redirectUrl': 'auth/user/login'},401)
                    # Check if the token is expired
                    if self._userToken.is_user_token_expired(user_token):
                        session.clear()
                        logout_user()
                        session['current_route'] = 'data_science.project.emotion_detector' 


                    comment = request.form.get('comment', None)
                    if comment is None or comment == '':
                        status = 400
                        message = 'Enter a comment to analyse'
                        category = 'error'
                    elif comment is None or comment == '':
                        status = 400
                        message = 'Enter a comment to analyse'
                        category = 'error'
                    elif not comment or not isinstance(comment, str):
                        status = 400
                        message = 'Enter a valid comment to analyse'
                        category = 'error'
                    elif self._emotionDetector.validate_string_with_digits(comment) == False:
                        status = 400
                        message = 'Enter a valid comment with with no special characteres to analyse'
                        category = 'error'
                    else:
                        status = 200
                        message = ''
                        category = 'success'
                        emotions = self._emotionDetector.emotion_detector(comment)

                    return jsonify({"message": message, "category": category, 'emotions': [emotions]},status)

        
        return render_template(self._template, title="Emotion Detector", user_token=user_token)

