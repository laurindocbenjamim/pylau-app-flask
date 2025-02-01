
import smtplib
import ssl
import os
import traceback
import sys

from flask import current_app
from flask_mail import Mail, Message

# Import the email modules we'll need
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.configs_package.modules.smtp_config import _get_smtp_config
from app.configs_package.modules.logger_config import get_message as set_logger_message
from app.utils.catch_exception_information import _catch_sys_except_information


mail = Mail()



def send_simple_email(subject, recipients, body, is_file=False) -> None:
     # Create the container email message.

    try:
        SMTP_HOST = current_app.config['SMTP_HOST']
        SMTP_PORT = current_app.config['SMTP_PORT']# ]587 by default
        SMTP_USER = current_app.config['SMTP_USER']
        SMTP_PASSWORD = current_app.config['SMTP_PASSWORD']
        #= _get_smtp_config()

        """
        with open(body, "r") as fp:
            # Create a text/plain message
            msg = EmailMessage() 
            msg.set_content(fp.read())
        """
        
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = recipients
            
        # Send the message via our own SMTP server.
        # FOR SMTP only the port is 587
        s = smtplib.SMTP(SMTP_HOST, SMTP_PORT,  timeout=60)
        #s = smtplib.SMTP_SSL(smtp_host, smtp_port, context=context)
        s.ehlo()
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.send_message(msg)
        s.set_debuglevel(1)
        s.quit()
        return True, 200
    except smtplib.SMTPServerDisconnected:
        s.connect(SMTP_HOST, SMTP_PORT)
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        custom_message = "Failed to connect to SMTP. Reconnecting..."
        error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="send_simple_email", custom_message=custom_message)
        set_logger_message(error_info)
        return False, type(e).__name__
    except Exception as e:
        custom_message = "General error"
        error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="send_simple_email", custom_message=custom_message)
        set_logger_message(error_info)
        return False, type(e).__name__
    

def send_simple_email_mime_multipart(subject, recipients, body, is_file=False) -> None:
     # Create the container email message.

    context = ssl.create_default_context()
    #smtp_host, smtp_port, smtp_user, smtp_password = _get_smtp_config()
    SMTP_HOST = current_app.config['SMTP_HOST']
    SMTP_PORT = current_app.config['SMTP_PORT']# ]587 by default
    SMTP_USER = current_app.config['SMTP_USER']
    SMTP_PASSWORD = current_app.config['SMTP_PASSWORD']
    message = """\
    This email was sent in order to check 
    your email is working properly."""
    conn = None 
    res = None
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = recipients 
        msg['Subject'] = subject
        
        part1 = MIMEText(message, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Connectiong to the SMTP server using SSL sending the email
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=60) as server:
            conn = server.login(SMTP_USER, SMTP_PASSWORD)
            res = server.sendmail(SMTP_USER, recipients, msg.as_string())
            server.set_debuglevel(1)
            server.quit()
            
            return True, 200
    except smtplib.SMTPServerDisconnected as e:
        #server.connect(SMTP_HOST, SMTP_PORT)
        #server.starttls()
        #server.login(SMTP_USER, SMTP_PASSWORD)
        custom_message = f"Failed to connect to SMTP. Reconnecting..."
        error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="send_simple_email_mime_multipart", custom_message=custom_message)
        set_logger_message(error_info)
        return False, custom_message
    except Exception as e:
        custom_message = "General error"
        error_info = _catch_sys_except_information(sys=sys, traceback=traceback, location="send_simple_email_mime_multipart", custom_message=custom_message)
        set_logger_message(error_info)
        return False, type(e).__name__
    