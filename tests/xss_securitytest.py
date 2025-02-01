import unittest
from flask import Flask, render_template_string

class XSSSecurityTest(unittest.TestCase):
    """
    This class contains unit tests for XSS (Cross-Site Scripting) security.
    """

    def setUp(self):
        self.app = Flask(__name__)

    def test_xss_protection(self):
        @self.app.route('/')
        def index():
            user_input = '<script>alert("XSS Attack!");</script>'
            return render_template_string('{{ user_input }}')

        with self.app.test_client() as client:
            response = client.get('/')
            self.assertNotIn('<script>', response.data.decode())

if __name__ == '__main__':
    unittest.main()
