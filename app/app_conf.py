import os
import secrets

def set_app_config(app):    
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config.from_mapping(
        SECRET_KEY= "o5NyiLAg5zpk0HsUv26PxOfa2VaV_f6oGxe6cDJO2is", # KEY GENERATED WITH secrets.token_urlsafe(32) 32 byts
    )

    # Set Email configurations
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'rocketmc2009@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jgtkeopkbwoxkjoo'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
