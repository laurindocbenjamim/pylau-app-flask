import smtplib
from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
import click  # Import the click module

# Import the email modules we'll need
from email.message import EmailMessage

from core.smtpmodule.emailcontroller import send_simple_email, send_simple_email_mime_multipart
from core.smtpmodule.send_html_email import send_an_html_email
from core.smtpmodule.html_content.activate_account_message_html import get_activate_account_message_html

bp = Blueprint("email", __name__, url_prefix='/email')
CORS(bp)


mail = Mail()

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
    
# Send an html email 
@bp.route('/smtplib/html/send', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def send_html_email():
    if request.method == 'GET':
        email = request.form.get('email', None)
        emailstatus = False

        textfile = "core/static/email_templates/email_.txt"
        
        resp = send_an_html_email('Email test 4', 'lucindadiasbenjamim@gmail.com', 2, "Laurindo Tester", "Just a test", '')
        return jsonify([{'emailstatus': resp, 'emailcode': 0 }])

@bp.route('/smtplib/send/simple', methods=['GET', 'POST'])
@cross_origin(methods=['GET', 'POST'])
def smtp_send_simple_email():
    if request.method == 'GET':
        textfile = "core/static/email_templates/email_.txt"
        body = "Hello brother"
        html = get_activate_account_message_html("Laurindo")
        res = send_simple_email_mime_multipart('Testing HTML - P9', "lucindadiasbenjamim@gmail.com", html, False)
        #res = send_simple_email('Testing with SSL', "lucindadiasbenjamim@gmail.com", textfile, False)
        return jsonify([{'emailstatus': res, 'emailcode': 0 }])


# Creating commands
@bp.cli.command("send_email")
@click.argument('email')
def send_s_mail(email):

    html = get_activate_account_message_html(email)
    res = send_simple_email_mime_multipart('Email test', email, html, False)
   
    return jsonify([{'emailstatus': res, 'emailcode': 0 }])