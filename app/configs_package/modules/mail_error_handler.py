import logging
from logging.handlers import SMTPHandler

def notify_email_error():
    mail_handler = SMTPHandler(
        mail_handler = '127.0.0.1',
        
    )