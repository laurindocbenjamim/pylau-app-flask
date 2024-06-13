

from flask import Blueprint, session
from .views.sendCodeEmailView import SendCodeEmailView
from .views.sendQrCodeEmailView import SendQrCodeEmailView
from .views.verifyOtpCodeView import VerifyOtpCodeView
from .views.verifyAppCodeAuthView import VerifyAppCodeAuthView
from ..two_factor_auth_module.twoFAModel import TwoFAModel

bp = Blueprint('email', __name__, url_prefix='/email')

kwargs = {
    'email': 'rocketmc2009@gmail.com',    
    'firstname': 'Laurindo',
    'lastname': "laurindo",
}

# routes to generate authentication code
bp.add_url_rule('/2fa-code/send', view_func=SendCodeEmailView.as_view('2facodesend', TwoFAModel, template='auth/2fa.html'))
bp.add_url_rule('/2fa-app/qr-code/send', view_func=SendQrCodeEmailView.as_view('2fappqrcodesend', TwoFAModel, template='auth/2fa_qrcode.html'))

# routes to verify authentication code
bp.add_url_rule('/2fa-code/verify', view_func=VerifyOtpCodeView.as_view('2facodeverify', TwoFAModel, template='auth/2fa.html'))
bp.add_url_rule('/2fa-app/qr-code/verify', view_func=VerifyAppCodeAuthView.as_view('2fappqrcodeverify', TwoFAModel, template='auth/2fa_qrcode.html'))
