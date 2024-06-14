

from flask import Blueprint, session
from .views.sendCodeEmailView import SendCodeEmailView
from .views.sendQrCodeEmailView import SendQrCodeEmailView
from .views.verifyOtpCodeView import VerifyOtpCodeView
from .views.getQrCodeEmailView import GetQrCodeEmailView
from .views.verifyAppCodeAuthView import VerifyAppCodeAuthView
from .views.sendActivateEmailView import SendActivateEmailView
from ..two_factor_auth_module.twoFAModel import TwoFAModel
from ..user_module.model.users import Users

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
bp.add_url_rule('/2fa-code/verify', view_func=VerifyOtpCodeView.as_view('2facodeverify', TwoFAModel, Users, template='auth/2fa.html'))
bp.add_url_rule('/2fa-app/qr-code/get/<string:token>', view_func=GetQrCodeEmailView.as_view('2fappqrcodeget', TwoFAModel, Users, template='auth/2fa_qrcode_display.html'))
bp.add_url_rule('/2fa-app/qr-code/verify', view_func=VerifyAppCodeAuthView.as_view('2fappqrcodeverify', TwoFAModel, Users, template='auth/2fa_qrcode.html'))

# route to send activation email
bp.add_url_rule('/activate/send', view_func=SendActivateEmailView.as_view('activate_send'))
