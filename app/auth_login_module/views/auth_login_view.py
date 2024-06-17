import flask
from flask_login import login_user, logout_user, current_user
from flask.views import View
from flask import render_template, request, session, redirect, url_for, flash, jsonify
from ..controller.authController import validate_form_fields

class AuthLoginView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, UserTokenModel, TwoFaModel, template):
        self.model = model
        self.UserTokenModel = UserTokenModel
        self.TwoFaModel = TwoFaModel
        self.template = template

    def dispatch_request(self):

        # Check if the user is already logged in
        if 'user_token' in session:
            if session['user_token'] :
                return redirect(url_for('index', user_token=session['user_token']))

        # Check if the user is already logged in
        if request.method == 'POST':
            if validate_form_fields(request.form):
                
                username = request.form.get('username')
                password = request.form.get('password')
                status, user = self.model.get_user_by_email(username)
                
                # First check if the user exists
                if status and user:

                    # Check if the user has a Token 
                    status, u_token = self.UserTokenModel.get_token_by_user(user.email)
                    
                    if status and u_token:

                        # Check if the user has two-factor authentication enabled
                        status, two_fa = self.TwoFaModel.get_user_two_fa_data(user.userID)
                        if status and two_fa:                           
                            # Check if the user password is correct
                            if user and user.check_password(password):
                                # Check if the user is activated
                                
                                if user.is_active() == True:
                                    
                                    # generate a secret code for the user
                                    status, u_token = self.UserTokenModel.update_token(user.userID, user.email)              
                                    #return jsonify({'status': u_token, 'message': u_token.exp_date, 'user_token': u_token.token})
                                    if status and u_token:
                                        # Create an object of the TwoFAModel class
                                        flask.session['user_token'] = u_token.token
                                        flask.session['user_id'] = user.userID
                                        flask.session['active'] = user.active
                                        flask.session['email'] = user.email
                                        flask.session['lastname'] = user.lastname
                                        flask.session['firstname'] = user.firstname
                                        flask.session['two_fa_auth_method'] = two_fa.method_auth
                                        flask.session['origin_request'] = 'signin'

                                        if two_fa.method_auth == 'app':
                                             return redirect(url_for('auth.user.app-otp-verify', user_token=u_token.token))
                                        elif two_fa.method_auth == 'email':
                                            return redirect(url_for('auth.user.send-otp-email', user_token=u_token.token)) 
                            
                                logout_user()
                                flask.flash('This user is not activated', 'danger')
                            else:
                                flask.flash('Invalid username or password ', 'error')
                else:
                    flask.flash('Username not found', 'error')

        return render_template(self.template, title='Login')