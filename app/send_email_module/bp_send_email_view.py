

from flask import Blueprint, session
from .sendCodeEmailView import SendCodeEmailView
from .sendQrCodeEmailView import SendQrCodeEmailView
from ..two_factor_auth_module.twoFAModel import TwoFAModel

bp = Blueprint('email', __name__, url_prefix='/email')

kwargs = {
    'email': 'rocketmc2009@gmail.com',    
    'firstname': 'Laurindo',
    'lastname': "laurindo",
}


bp.add_url_rule('/verify-code/send', view_func=SendCodeEmailView.as_view('verify_code_send', TwoFAModel, template='auth/2fa.html'))
bp.add_url_rule('/verify/qr/code/send', view_func=SendQrCodeEmailView.as_view('verify_qr_code_send', TwoFAModel, template='auth/2fa_qrcode.html'))
