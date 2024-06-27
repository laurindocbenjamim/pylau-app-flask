
import os

def _get_smtp_config() -> tuple:

    # Get the SMTP configuration from the environment variables
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_port = int(os.environ.get('SMTP_PORT')) # 587 by default
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    # Yandex configurations
    """smtp_host = os.environ.get('SMTP_HOST', 'smtp.yandex.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 465)) # 465 for SSL
    smtp_user = os.environ.get('SMTP_USER', 'data-tuning@yandex.com')
    smtp_password = os.environ.get('SMTP_PASSWORD', 'aecnrbosvgdvahzw')
"""
    return smtp_host, smtp_port, smtp_user, smtp_password