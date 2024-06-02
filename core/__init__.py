from core.app import db, create_application
from core.models.personmodel import Person
from core.authmodule.UserModel import User
from core.authmodule.UserController import (
    create_user, get_users, get_user_by_id, 
    update_user, delete_user, get_user_by_email,
    check_email_exists, check_phone_exists
)
from core.authmodule.repositories.uservalidation import validate_form_fields, is_valid_email
from core.controller.personController import create_person, get_all_people, get_person_by_id