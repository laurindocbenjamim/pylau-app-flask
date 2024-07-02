
# The copmmand to run this tests file is
# $: python -m pytest -s module.py
# or just
# $: python -m pytest
from ..app import create_application

def test_config():
    assert not create_application().testing
    assert not create_application(None, {'TESTING':True}).testing


def hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World'
    
