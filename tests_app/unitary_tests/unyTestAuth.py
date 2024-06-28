import unittest

#from ...app.auth_module.sign_up_sub_module.model.users import Users
from ...app.auth_package.module_sign_up_sub.controller.userController import load_user_obj, validate_form_fields
from app.auth_package import Users

from werkzeug.security import generate_password_hash
from datetime import datetime, timezone


class TestAuth(unittest.TestCase):

    def sign_up(self):
       
        data = Users(
             firstname = "Unitary",
            lastname = "Test",
            username = "user",
            email = "uitarytest@gmail.com",
            country = "test",
            country_code = "+333",
            phone = "dd",
            password = generate_password_hash("wwwww"),        
            role = "test",
            active = False
        )
        response = Users.create_user(data)
        self.assertEqual(response,True)



if __name__ == '__main__':
    unittest.main()
    