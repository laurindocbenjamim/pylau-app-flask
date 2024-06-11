
import smtplib
import ssl
import os

from flask_mail import Mail, Message

# Import the email modules we'll need
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..configs.smtp_config import _get_smtp_config


mail = Mail()



def send_simple_email(subject, recipients, body, is_file=False) -> None:
     # Create the container email message.

    try:
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
        return True
    except Exception as e:
        return f"Error: {e}"
    

def send_simple_email_mime_multipart(subject, recipients, body, is_file=False) -> None:
     # Create the container email message.

    context = ssl.create_default_context()
    smtp_host, smtp_port, smtp_user, smtp_password = _get_smtp_config()
    message = """\
    This email was sent in order to check 
    your email client if it is working properly."""
    
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipients 
        msg['Subject'] = subject
        
        part1 = MIMEText(message, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Connectiong to the SMTP server using SSL sending the email
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipients, msg.as_string())
            return True
    except Exception as e:
        #print(f"Error: {e}")
        return type(e).__name__
    