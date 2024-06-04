
import re

from datetime import date
from flask import jsonify, render_template, redirect, url_for

from core import create_user

from core import get_user_by_email, get_user_by_id

from core.config import verify_provisioning_uri, update_imagename


def create_final_user(db,firstname, lastname, email, country,country_code, phone, password_hash, secret, otpqrcode):

    try:
        user = create_user(db,firstname, lastname, email, country,country_code, phone, password_hash, secret)
        if user.userID is not None:
            img = otpqrcode
            current_date = date.today()
            new_image_name = secret +'-otpqrcode-done-'+current_date.strftime("%Y-%m-%d")
            #update_imagename('core/static/otp_qrcode_images/' + img, new_image_name)

            return jsonify({'message': 'User is ready to be created successfully!', 'status': 3, 'otpstatus':None, 
                                        "object": [], "redirectUrl": "auth/2fapp/login"}, 200)
        else:              
            return jsonify({'message': 'Failed to regist user', 'status': 'error', "redirectUrl": "users/create"}, 400)
    except Exception as e:
        return jsonify({'message': 'Error: '+e, 'status': 'error', "redirectUrl": "users/create"}, 400) 
    
   
def create_final_user_2(db,firstname, lastname, email, country,country_code, phone, password_hash, OTP, secret, otpqrcode):

    if len(OTP) != 6:
        return jsonify({'message': 'Maximum digits required for the 2FA code is 6.', 'status': 'error', "redirectUrl": "users/create"}, 400)
    else:

        #OTP = request.form.get('two_factor_auth_code')
        #secret = request.form.get('secret')
                    
        otpstatus = False
        if OTP is not None and secret is not None:
            otpstatus = verify_provisioning_uri(secret, OTP)

            if otpstatus:
                            
                try:
                    user = create_user(db,firstname, lastname, email, country,country_code, phone, password_hash, secret)
                    if user.userID is not None:
                        img = otpqrcode
                        current_date = date.today()
                        new_image_name = secret +'-otpqrcode-done-'+current_date.strftime("%Y-%m-%d")
                        update_imagename('core/static/otp_qrcode_images/' + img, new_image_name)

                        return jsonify({'message': 'User is ready to be created successfully!', 'status': 3, 'otpstatus':otpstatus, 
                                        "object": [], "redirectUrl": "auth/2fapp/login"}, 200)
                    else:              
                        return jsonify({'message': 'Failed to regist user', 'status': 'error', "redirectUrl": "users/create"}, 400)
                except Exception as e:
                    return jsonify({'message': 'Error: '+e, 'status': 'error', "redirectUrl": "users/create"}, 400) 
                        
            else:
                return jsonify({'message': '2FA OTP code is invalid.', 'status': 'error', "redirectUrl": "users/create"}, 400)
        else:                 
            return jsonify({'message': '2FA OTP code not found.', 'status': 'error', 'otpstatus':otpstatus, 
                                    "object": [], "redirectUrl": "users/create"}, 400)

            
                # create a user