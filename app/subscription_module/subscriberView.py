
from cmath import e
from flask.views import View
from flask import request, flash,url_for, redirect, session, jsonify
from ..utils import is_valid_email
from ..email_module import send_simple_email_mime_multipart
from ..email_module import get_subscriber_message_html

class SubscriberView(View):
    methods = ['GET', 'POST']

    def __init__(self, subscriberModel):
        self.subscriberModel = subscriberModel  

    def dispatch_request(self):
        subscriber = ''
        status = 200
        message = '?'
        category = '?'
        user_token = session['user_token'] if 'user_token' in session and session['user_token'] is not None else ''
        if request.method == 'POST':
            email = request.form.get('email', None)
            
            if email is not None and len(email) <= 200:
                
                if is_valid_email(email):

                    status, obj = self.subscriberModel.check_subscriber(email)
                    if status:
                        email_not_exists = True
                        try:
                            email_not_exists = False if obj.email == str(email) else False
                        except Exception:
                            email_not_exists = True
                        
                        if email_not_exists:
                            resp, obj = self.subscriberModel.save_subscriber(email)
                            if resp:
                                html = get_subscriber_message_html(str(email))
                                status = send_simple_email_mime_multipart("Welcome subscriber", str(email), html )
                                status = 200
                                message = 'Submited successfully'
                                category = 'success'
                                subscriber = email
                            else:
                                status = 406
                                message = 'Error on submition'
                                category = 'error'
                                subscriber = 'obj'
                        else:
                            status = 200
                            message = 'Subscription already exists'
                            category = 'info'
                            subscriber = len(obj.to_dict())
                    else:
                        status = 400
                        message = 'Failed to Subscribe the page'
                        category = 'error'
                        subscriber = ''
                    
                else:
                    flash('Invalid email. Email accepted: @gmail.com, @hotmail.com, @outlook.com, @icloud.com, @live.com')
                    message = 'Invalid email. Email accepted: @gmail.com, @hotmail.com, @outlook.com, @icloud.com, @live.com'
                    category = 'error'
                    status = 400
            else:
                flash('Enter an email to subscribe')
                message = 'Enter an email to subscribe'
                category = 'error'
                status = 400


        #return redirect(url_for('index', user_token=user_token))
        return jsonify({"message": message, "category": category, "subscriber":subscriber},status)
