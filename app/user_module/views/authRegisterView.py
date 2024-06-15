
from flask.views import View
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from ..controller.userController import load_user_obj, validate_form_fields


class AuthRegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self, model, tokenModel, template):
        self.model = model
        self.template = template
        self.tokenModel = tokenModel

    def dispatch_request(self):
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
                        flash(f'Error creating token {token}', 'error')
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
                           
                            if two_fa_auth_method == 'app':                            
                                return redirect(url_for('email.2fappqrcodeget', token=token.token))                                 
                            else:                               
                                return redirect(url_for('email.2facodesend'))                           
                        else:
                            flash("Failed to create user", 'error')   
                        
                    
        return render_template(self.template, title='Register')