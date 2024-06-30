import os
import tempfile


import pytest
from app import create_application
from app import db


with open(os.path.join(os.path.dirname(__file__), 'data/data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    