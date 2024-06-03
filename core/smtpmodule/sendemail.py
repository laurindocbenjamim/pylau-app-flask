import smtplib
from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin

# Import the email modules we'll need
from email.message import EmailMessage

from core.smtpmodule.emailcontroller import send_simple_email, send_simple_email_with_yandex

bp = Blueprint("email", __name__, url_prefix='/email')
CORS(bp)


mail = Mail()


@bp.route('/flask/send', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def send_email():
    if request.method == 'GET':
        email = request.form.get('email', None)
        emailstatus = False

        msg = Message('Hello!')
        msg.sender = ('Hello on the other side!', 'laurindocbenjamim@gmail.com')
        msg.recipients=['rocketmc2009@gmail.com']
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)
        emailstatus = True
        return jsonify([{'emailstatus': emailstatus, 'emailcode': 000}])
    
    elif request.method == 'POST':
        email = request.form.get('email', None)
        emailstatus = False

        msg = Message('Hello!')
        msg.sender = ('Hello on the other side!', 'rocketmc2009@gmail.com')
        msg.recipients=['laurindocbenjamim@gmail.com']
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)
        emailstatus = True
        return jsonify([{'emailstatus': emailstatus, 'emailcode': 000}])

@bp.route('/smtplib/send', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def smtp_send_email():
    if request.method == 'GET':
        email = request.form.get('email', None)
        emailstatus = False

        textfile = "core/static/email_templates/email_.txt"
        # Create the container email message.
        with open(textfile, "r") as fp:
            # Create a text/plain message
            msg = EmailMessage()
            msg.set_content(fp.read())
        
        # First way to send email
        #s = smtplib.SMTP('smtp.gmail.com', 587)
        #s.starttls()
        #s.login("iledmd3@gmail.com", "aecnrbosvgdvahzw")

        # Second way to send email
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = f'Test email from Flask using smtplib'
        msg['From'] = "iledmd3@gmail.com"
        msg['To'] = "lucindadiasbenjamim@gmail.com"

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login("iledmd3@gmail.com", "aecnrbosvgdvahzw")
        emailstatus = s.send_message(msg)
        s.quit()
        return jsonify([{'emailstatus': emailstatus, 'emailcode': 000}])
    

@bp.route('/smtplib/send/simple', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def smtp_send_simple_email():
    if request.method == 'GET':
        textfile = "core/static/email_templates/email_.txt"
        body = "Hello brother"
        res = send_simple_email_with_yandex('Testing with SSL', "lucindadiasbenjamim@gmail.com", textfile, False)
        #res = send_simple_email('Testing with SSL', "lucindadiasbenjamim@gmail.com", textfile, False)
        return jsonify([{'emailstatus': res, 'emailcode': 0 }])