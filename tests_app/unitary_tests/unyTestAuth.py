import unittest

#from ...app.auth_module.sign_up_sub_module.model.users import Users
#from ...app.auth_package.module_sign_up_sub.controller.userController import load_user_obj, validate_form_fields
#from app.auth_package import Users

from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
class Users(object):

    def __init__(self, user, age) -> None:
        self._user = user
        self._age = age

    def create_user(data):
        resp =f'Username is {data._user} Age: {data._age}' 
        try:
            if data._user is None or data._user == "":
                return False
            elif data._age is None or int(data._age) <= 0 or data._age == "":
                return False
            return True
        except Exception as e:
            return False

class TestAuth(unittest.TestCase):

    def test_create_user(self):
       
        data = Users(
            user = "ll",
            age = 10
        )
        response = Users.create_user(data)
        self.assertEqual(response,True)



if __name__ == '__main__':
    unittest.main()
    