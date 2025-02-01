import flask
from flask import render_template, jsonify, abort, session

from .authLoginView import AuthLoginView
from .logoutView import LogoutView
from app.token_module import UserToken
from app.two_factor_auth_module import TwoFAModel
from .sendAuthCodeEmailView import SendAuthCodeEmailView
from .verifyAuthOtpCodeView import VerifyAuthOtpCodeView
from .verifyAppAuthCodeView import VerifyAppAuthCodeView
from .authUserHistoric import AuthUserHistoric

from flask_login import logout_user



bp_auth = flask.Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

def init_login_app(login_manager, db):
    
    from ...module_sign_up_sub.model.users import Users

    """
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
       
    
    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('username')
        
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.is_active() == True:
                # Use the login_user method to log in the user  
                if 'user_token' in flask.session:
                    return flask.redirect(flask.url_for('index', user_token=flask.session['user_token']))   
        return 
        
    
    """
    
    
    """
        @login_manager.unauthorized_handler
        def unauthorized_handler():
            flask.session.clear()        
            return render_template('errors/401.html')
    """
        
    
    
    bp_auth.add_url_rule('/login', view_func=AuthLoginView.as_view('login', Users, UserToken, TwoFAModel, AuthUserHistoric,  template='auth/auth.html'))
    bp_auth.add_url_rule('/send-otp/email/<string:user_token>', view_func=SendAuthCodeEmailView.as_view('send-otp-email', UserToken, Users, TwoFAModel, template='auth/2fa.html'))
    bp_auth.add_url_rule('/otp/verify/<string:user_token>', view_func=VerifyAuthOtpCodeView.as_view('verify-otp',  UserToken, Users, TwoFAModel, AuthUserHistoric, template='auth/2fa.html'))
    bp_auth.add_url_rule('/app-otp/verify/<string:user_token>', view_func=VerifyAppAuthCodeView.as_view('app-otp-verify',  UserToken, Users, TwoFAModel, AuthUserHistoric, template='auth/2fa_qrcode.html'))
    
    #Logout route
    @bp_auth.route('/logout')
    def logout():
        status, obj = AuthUserHistoric.update_auth_user(session.get('user_id'), session.get('email'), False)
        re, obj2 = UserToken.expire_the_user_token_by_user(session.get('email'), session.get('user_token'))
        
        resp, exp_token = UserToken.force_user_jwt_token_expiration(str(session.get('user_token', '')))
        
        session.clear()
        logout_user()
        
        return flask.redirect(flask.url_for('auth.user.login'))

    bp_auth.add_url_rule('/logout/<string:user_token>', view_func=lambda:LogoutView.as_view('logout', UserToken, AuthUserHistoric))
    
