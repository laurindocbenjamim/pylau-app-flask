
import smtplib

from email.mime.text import MIMEText
from .smtp_config import _get_smtp_config
from core.smtpmodule.html_content.activate_account_message_html import get_activate_account_message_html
from jinja2 import Template

def send_an_html_email(subject, recipients, user_id, name, message, html_file):
    smtp_host, smtp_port, smtp_user, smtp_password =_get_smtp_config()
    try:
        
        # Rest of the code for sending and formatting the email

        body = get_activate_account_message_html(name)
        #html_message = MIMEText(body, "html")
        html_message = MIMEText()
        html_message['Subject'] = subject
        html_message['From'] = smtp_user
        html_message['To'] = recipients
        html_message.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipients, html_message.as_string())
            return True

    except Exception as e:
        #print(f"An error occurred while sending the email: {str(e)}")
        return f"An error occurred while sending the email: {type(e)}"
