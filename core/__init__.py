from core.app import db, create_application
from .models.personmodel import Person
from .authmodule.UserModel import User
from .authmodule.UserController import create_user, get_users, get_user_by_id, update_user, delete_user, check_email_exists, check_phone_exists
from .controller.personController import create_person, get_all_people, get_person_by_id