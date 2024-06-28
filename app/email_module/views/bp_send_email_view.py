

from flask import Blueprint, session
from .sendCodeEmailView import SendCodeEmailView
from .sendQrCodeEmailView import SendQrCodeEmailView
from .verifyOtpCodeView import VerifyOtpCodeView
from .getQrCodeEmailView import GetQrCodeEmailView
from .verifyAppCodeAuthView import VerifyAppCodeAuthView
from .sendActivateEmailView import SendActivateEmailView
from ...two_factor_auth_module.twoFAModel import TwoFAModel
from ...auth_package.module_sign_up_sub.model.users import Users
from ...token_module.userTokenModel import UserToken

bp = Blueprint('email', __name__, url_prefix='/email')


# routes to generate authentication code
bp.add_url_rule('/2fa-code/send/<string:user_token>', view_func=SendCodeEmailView.as_view('2facodesend',UserToken, Users, TwoFAModel, template='auth/2fa.html'))
bp.add_url_rule('/2fa-app/qr-code/send/<string:user_token>', view_func=SendQrCodeEmailView.as_view('2fappqrcodesend', TwoFAModel, template='auth/2fa_qrcode.html'))

# routes to verify authentication code
bp.add_url_rule('/2fa-code/verify/<string:user_token>', view_func=VerifyOtpCodeView.as_view('2facodeverify', UserToken, Users, TwoFAModel, template='auth/2fa.html'))
bp.add_url_rule('/2fa-app/qr-code/get/<string:user_token>', view_func=GetQrCodeEmailView.as_view('2fappqrcodeget', UserToken, Users, TwoFAModel, template='auth/2fa_qrcode_display.html'))
bp.add_url_rule('/2fa-app/qr-code/verify/<string:user_token>', view_func=VerifyAppCodeAuthView.as_view('2fappqrcodeverify',  UserToken, Users, TwoFAModel, template='auth/2fa_qrcode.html'))

# route to send activation email
bp.add_url_rule('/activate/send/<string:user_token>', view_func=SendActivateEmailView.as_view('activate_send', UserToken, Users))
