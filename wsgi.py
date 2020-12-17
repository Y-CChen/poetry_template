from config import Config
from flask_template import make_app

app = make_app(Config, False).app
