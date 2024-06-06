from core.app import db, create_application
from core.config import token_required, generate_token, decode_token, token_required
from core.config.clear_sessions import clear_all_sessions

from core.factory.two_factor_auth_factory import generate_simple_otp, check_simple_otp
from core.models.personmodel import Person
from core.authmodule.models.UserModel import User
from core.authmodule.models.TwoFAModel import TwoFAModel
from core.tokenmodule.tokenmodel import Token
from core.tokenmodule.tokencontroller import create_token, get_token_by_id, get_token_by_token, delete_token

from core.authmodule.controllers.UserController import (
    create_user, get_users, get_user_by_id,
    get_user_by_id_limited_dict, 
    update_user, update_user_status, delete_user, get_user_by_email,
    check_email_exists, check_phone_exists
)
from core.authmodule.controllers.two_factor_auth_controller import get_two_fa_by_user_id

from core.smtpmodule.emailcontroller import send_simple_email, send_simple_email_mime_multipart

from core.authmodule.repositories.uservalidation import validate_form_fields, is_valid_email
from core.controller.personController import create_person, get_all_people, get_person_by_id