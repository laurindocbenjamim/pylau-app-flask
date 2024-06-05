
import os

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