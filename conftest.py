import pytest

from config import Config
from flask_template import make_app


@pytest.fixture
def app():
    app, with_app_context_wraps = make_app(Config, False)
    return app
