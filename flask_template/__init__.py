__version__ = "0.1.0"
from collections import namedtuple
from functools import wraps

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    # api
    from . import resources

    app.register_blueprint(resources.root.blueprint)
    url_prefix = app.config["APP_URL_PREFIX"]
    app.register_blueprint(resources.sitemap.blueprint, url_prefix=url_prefix)

    return App
