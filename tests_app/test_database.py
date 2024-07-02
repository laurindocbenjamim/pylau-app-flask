
# The copmmand to run this tests file is
# $: python -m pytest -s module.py
# or just
# $: python -m pytest

import sqlite3
import pytest
from sqlalchemy import and_, text


def test_get_close_sql_alchemy_db(app):
    from ..app import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    with pytest.raises(sqlite3.ProgrammingError) as e:
        response = db.session.execute(text('SELECT date'))
        db.session.commit()

    assert 'closed' in str(e.value)

def test_get_close_db(app):    
    from ..app import db
    with pytest.raises(sqlite3.ProgrammingError) as e:
        response = db.session.execute(text('SELECT date'))
        db.session.commit()

    assert 'closed' in str(e.value)


"""
This test uses Pytest’s monkeypatch fixture to replace the init_db 
function with one that records that it’s been called. .
"""
def test_init_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('app.db.init_app', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

        