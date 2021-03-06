import pytest
from project import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app({'SERVER_NAME': 'regit'})

    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client
    ctx.pop()
