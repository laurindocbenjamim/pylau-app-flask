
from flask.views import View
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from ..controller.userController import load_user_obj, validate_form_fields
from ...two_factor_auth_module.two_fa_auth_controller import load_two_fa_obj


class AuthRegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, tokenModel, twoFaModel, template):
        self.model = model
        self.template = template
        self.tokenModel = tokenModel
        self.twoFaModel = twoFaModel

    def dispatch_request(self):

        # Check if the user is already logged in
        if 'user_token' in session:
            if session['user_token'] != 'favicon.ico':
                return redirect(url_for('index', user_token=session['user_token']))
            
        if request.method == 'POST':

            # Validate form fields
            if validate_form_fields(request.form):                

                # Check if email exists
                if self.model.check_email_exists(request.form.get('email')):
                    flash('Email already exists', 'info')
                
                # Check if phone exists
                elif self.model.check_phone_exists(request.form.get('phone')):
                    flash('Phone already exists', 'info')

                # If email and phone do not exist, create user
                else:

                    # bEFORE CREATE User generate and save token
                    token = self.tokenModel.create_token(request.form.get('email'))
                    if token == False:
                        self.model.db.session.rollback()
                        flash('Error creating token.', 'error')
                    else:      

                        status,last_user_id = self.model.create_user(load_user_obj(request.form, 'user'))
                        if status:
                                                      
                            two_fa_auth_method = request.form.get('two_fa_auth_method')
                            
                            session['origin_request'] = 'register'
                            session['two_fa_auth_method'] = two_fa_auth_method
                            session['user_token'] = token.token                            
                            session['user_id'] = last_user_id
                            session['firstname'] = request.form.get('firstname')
                            session['lastname'] = request.form.get('lastname')
                            session['email'] = request.form.get('email')

                            # Create an object of the TwoFAModel class
                                 
                            # Call the method with the required data
                            two_fa_obj = load_two_fa_obj({
                                'userID': last_user_id,
                                'two_factor_auth_secret': '',
                                'method_auth': two_fa_auth_method,
                                'is_active': True
                            })

                            # Save the secret code in the database
                            respTwoFa, obj = self.twoFaModel.save_two_fa_data(two_fa_obj)

                            if two_fa_auth_method == 'app':  
                                return redirect(url_for('email.2fappqrcodeget', user_token=token.token))                                 
                            else:                               
                                return redirect(url_for('email.2facodesend', user_token=token.token))                           
                        else:
                            flash("Failed to create user", 'error')   
                        
                    
        return render_template(self.template, title='Register')
    
    