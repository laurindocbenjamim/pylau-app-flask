import os
import tempfile


import pytest
from ..app import create_application
from ..app import db


with open(os.path.join(os.path.dirname(__file__), 'data/data.sql'), 'rb') as f:
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


    