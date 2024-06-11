

from flask import Blueprint, session
from .sendCodeEmailView import SendCodeEmailView

bp = Blueprint('email', __name__, url_prefix='/email')

kwargs = {
    'email': 'rocketmc2009@gmail.com',    
    'firstname': 'Laurindo',
    'lastname': "laurindo",
}


bp.add_url_rule('/send', view_func=SendCodeEmailView.as_view('send', template='auth/2fa.html'))
