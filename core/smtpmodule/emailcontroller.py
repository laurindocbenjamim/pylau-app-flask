
import smtplib
import ssl
import os

from flask_mail import Mail, Message

# Import the email modules we'll need
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



mail = Mail()

def _get_smtp_config() -> tuple:

    # Get the SMTP configuration from the environment variables
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 465)) # 587 by default
    smtp_user = os.environ.get('SMTP_USER', 'iledmd3@gmail.com')
    smtp_password = os.environ.get('SMTP_PASSWORD', 'aecnrbosvgdvahzw')

    # Yandex configurations
    """smtp_host = os.environ.get('SMTP_HOST', 'smtp.yandex.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 465)) # 465 for SSL
    smtp_user = os.environ.get('SMTP_USER', 'data-tuning@yandex.com')
    smtp_password = os.environ.get('SMTP_PASSWORD', 'aecnrbosvgdvahzw')
"""
    return smtp_host, smtp_port, smtp_user, smtp_password

def send_simple_email(subject, recipients, body, is_file=False) -> None:
     # Create the container email message.

    smtp_host, smtp_port, smtp_user, smtp_password = _get_smtp_config()

    with open(body, "r") as fp:
        # Create a text/plain message
        msg = EmailMessage() 
        msg.set_content(fp.read())
      
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipients
        
    # Send the message via our own SMTP server.
    s = smtplib.SMTP(smtp_host, smtp_port)
    #s = smtplib.SMTP_SSL(smtp_host, smtp_port, context=context)
    s.ehlo()
    s.starttls()
    s.login(smtp_user, smtp_password)
    s.send_message(msg)
    s.quit()

def send_simple_email_with_yandex(subject, recipients, body, is_file=False) -> None:
     # Create the container email message.

    context = ssl.create_default_context()
    smtp_host, smtp_port, smtp_user, smtp_password = _get_smtp_config()

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipients 
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connectiong to the SMTP server using SSL sending the email
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipients, msg.as_string())
            return True
    except Exception as e:
        #print(f"Error: {e}")
        return False
    