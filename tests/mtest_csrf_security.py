import unittest
from flask import Flask
from flask_testing import TestCase

class MyTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['SECRET_KEY'] = 'your_secret_key'
        return app

    def test_csrf_protection(self):
        response = self.client.post('/some_route', data={'param': 'value'})
        self.assertRedirects(response, '/login')  # Assuming you have a login route

if __name__ == '__main__':
    unittest.main()