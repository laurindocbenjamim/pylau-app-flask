
from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin

bpapp = Blueprint("sendemail", __name__, url_prefix='/email')
CORS(bpapp)
mail = Mail()


@bpapp.route('/send', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def send_email():
    if request.method == 'GET':
        email = request.form.get('email')
        emailstatus = False

        msg = Message('Hello!')
        msg.sender = ('Hello on the other side!', 'laurindocbenjamim@gmail.com')
        msg.recipients=['rocketmc2009@gmail.com']
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)
        emailstatus = True
        return jsonify([{'emailstatus': emailstatus, 'emailcode': 000}])
    
    elif request.method == 'POST':
        email = request.form.get('email')
        emailstatus = False

        msg = Message('Hello!')
        msg.sender = ('Hello on the other side!', 'rocketmc2009@gmail.com')
        msg.recipients=['laurindocbenjamim@gmail.com']
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)
        emailstatus = True
        return jsonify([{'emailstatus': emailstatus, 'emailcode': 000}])

