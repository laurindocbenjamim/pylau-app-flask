
# The copmmand to run this tests file is
# $: python -m pytest -s module.py
# or just
# $: python -m pytest
from app import create_app
import pytest

"""
@pytest.fixture
def app():
    #db_fd, db_path = tempfile.mkstemp()
    return create_app()


"""

"""
The client fixture calls app.test_client() with 
the application object created by the app fixture. 
Tests will use the client to make requests to the application without running the server.
"""


"""
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

"""

def test_config():
    """
    
    """
    assert not create_app().testing
    assert create_app(test_config=True).testing


def test_hello(client):
    """
    
    """
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.data == b'Hello, World'

def test_new_post(client):
    """
    
    """
    response = client.get('/new-post')
    assert response.status_code == 200
    assert response.get_json() == {'post': "Hello world!"}
