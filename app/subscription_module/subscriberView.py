
from flask.views import View
from flask import request, flash,url_for, redirect, session, jsonify
from ..utils import is_valid_email

class SubscriberView(View):
    methods=['POST']

    def __init__(self, subscriberModel):
        self.subscriberModel = subscriberModel  

    def dispatch_request(self) -> None:
        user_token = session['user_token'] if 'user_token' in session and session['user_token'] is not None else ''
        if request.method == 'POST':
            email = request.form.get('email', None)

            if email is not None and len(email) <= 200:
                if is_valid_email(email):
                    status, obj = self.subscriberModel.save_subscriber(email)
                else:
                    flash('Invalid email')
            else:
                flash('Enter an email to subscribe')


        return redirect(url_for('index', user_token=user_token))
