from app import create_application

def test_hello():
    assert not create_application().testing
    assert create_application({'TESTING': True}).testing