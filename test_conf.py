
"""
This file is the entry point of the application, it is the file that will be executed by the server
"""

# The copmmand to run this tests file is
# $: python -m pytest -s module.py
# or just
# $: python -m pytest
import os
import tempfile

import pytest
from app import create_application
from app import db


with open(os.path.join(os.path.dirname(__file__), 'tests_app/data/data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    #db_fd, db_path = tempfile.mkstemp()

    app = create_application()


"""
The client fixture calls app.test_client() with 
the application object created by the app fixture. 
Tests will use the client to make requests to the application without running the server.
"""
@pytest.fixture
def client():
    return app.test_client()


"""
The runner fixture is similar to client. app.test_cli_runner() 
creates a runner that can call the Click commands registered with the application.
"""
@pytest.fixture
def runner():
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self,client):
        self._client = client
    
    def login(self, username='test', password='123'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')

"""
With the auth fixture, you can call auth.login() in a 
test to log in as the test user, which was inserted as part of the test data in the app fixture.
"""
@pytest.fixture
def auth(client):
    return AuthActions(client)






    