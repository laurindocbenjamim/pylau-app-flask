
from flask import Blueprint
from .recover_account_first_step_view import AccountRecoverFirstStepView
from .recover_account_second_step_view import AccountRecoverSecondStepView
from ..module_sign_up_sub.model.users import Users
from ...token_module.userTokenModel import UserToken
from ...two_factor_auth_module.twoFAModel  import TwoFAModel

bp_acc_recover = Blueprint('recover', __name__, url_prefix='recover')

bp_acc_recover.add_url_rule('/user-account', view_func=AccountRecoverFirstStepView.as_view('user_account',Users, UserToken, TwoFAModel, 'auth/recover_account_first_step.html'))
bp_acc_recover.add_url_rule('/user-account/<string:user_token>', view_func=AccountRecoverSecondStepView.as_view('user_account_st_2',Users, UserToken, TwoFAModel, 'auth/recover_account_second_step.html'))