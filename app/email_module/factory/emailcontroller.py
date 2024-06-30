
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
from ...configs_package.modules.logger_config import get_message as set_logger_message


mail = Mail()



def send_simple_email(subject, recipients, body, is_file=False) -> None:
     # Create the container email message.

    try:
        SMTP_HOST = current_app.config['SMTP_HOST']
        SMTP_PORT = current_app.config['SMTP_PORT']# ]587 by default
        SMTP_USER = current_app.config['SMTP_USER']
        SMTP_PASSWORD = current_app.config['SMTP_PASSWORD']
        #= _get_smtp_config()

        with open(body, "r") as fp:
            # Create a text/plain message
            msg = EmailMessage() 
            msg.set_content(fp.read())
        
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = recipients
            
        # Send the message via our own SMTP server.
        s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        #s = smtplib.SMTP_SSL(smtp_host, smtp_port, context=context)
        s.ehlo()
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.send_message(msg)
        s.quit()
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        set_logger_message(f"Error occured on method[save_two_fa_data]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")
        return type(e).__name__
    

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
    your email client if it is working properly."""
    
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
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipients, msg.as_string())
            return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        set_logger_message(f"Error occured on method[save_two_fa_data]: \n \
                                       Exception: {str(sys.exc_info())}\
                                       \nFile name: {fname}\
                                       \nExc-instance: {fname}\
                                       \nExc-classe: {exc_type}\
                                       \nLine of error: {exc_tb.tb_lineno}\
                                       \nTB object: {exc_tb}\
                                       \nTraceback object: {str(traceback.format_exc())}\
                                        ")
        return type(e).__name__
    