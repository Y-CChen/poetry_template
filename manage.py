from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from config import Config
from flask_template import db, make_app, models


def _main():
    app, with_app_context_wraps = make_app(Config, True)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
    manager.run()


if __name__ == "__main__":
    _main()
