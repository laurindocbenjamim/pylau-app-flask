import flask
from flask import render_template, jsonify

from .authLoginView import AuthLoginView
from .logoutView import LogoutView
from ...token_module.userTokenModel import UserToken
from ...two_factor_auth_module.twoFAModel import TwoFAModel
from .sendAuthCodeEmailView import SendAuthCodeEmailView
from .verifyAuthOtpCodeView import VerifyAuthOtpCodeView
from .verifyAppAuthCodeView import VerifyAppAuthCodeView
from .authUserHistoric import AuthUserHistoric

from flask_login import logout_user, login_user



bp_auth = flask.Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

def init_app(login_manager, db):
    
    from ...user_module import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)
       
    
    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('username')
        
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.is_active() == True:
                # Use the login_user method to log in the user  
                if 'user_token' in flask.session:
                    return flask.redirect(flask.url_for('projects.list', user_token=flask.session['user_token']))   
        return 
    
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        #return 'Unauthorized', 401
        return flask.redirect(flask.url_for('auth.user.login'))

    bp_auth.add_url_rule('/login', view_func=AuthLoginView.as_view('login', Users, UserToken, TwoFAModel,  template='auth/auth.html'))
    bp_auth.add_url_rule('/send-otp/email/<string:user_token>', view_func=SendAuthCodeEmailView.as_view('send-otp-email', UserToken, Users, TwoFAModel, template='auth/2fa.html'))
    bp_auth.add_url_rule('/otp/verify/<string:user_token>', view_func=VerifyAuthOtpCodeView.as_view('verify-otp',  UserToken, Users, TwoFAModel, AuthUserHistoric, template='auth/2fa.html'))
    bp_auth.add_url_rule('/app-otp/verify/<string:user_token>', view_func=VerifyAppAuthCodeView.as_view('app-otp-verify',  UserToken, Users, TwoFAModel, AuthUserHistoric, template='auth/2fa_qrcode.html'))
    bp_auth.add_url_rule('/logout/<string:user_token>', view_func=LogoutView.as_view('logout', UserToken, AuthUserHistoric))
    # Logout route
    #@bp_auth.route('/logout')
    #def logout():
        #AuthUserHistoric().update_auth_user(flask.session.get('user_id'), flask.session.get('email'), False)
        #flask.session.clear()
        #logout_user()
        
        #return flask.redirect(flask.url_for('auth.user.login'))

