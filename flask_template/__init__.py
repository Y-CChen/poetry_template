__version__ = "0.1.0"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from collections import namedtuple

db = SQLAlchemy()


def make_app(config, for_manage) -> Flask:
    app = Flask(__name__, static_folder=None)
    def with_app_context_wraps(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            with app.app_context():
                return function(*args, **kwargs)

        return wrapper

    App = namedtuple("App", ("app", "with_app_context_wraps"))(app, with_app_context_wraps)

    app.config.from_object(config)
    db.init_app(app)
    if for_manage:
        return App
    return App
