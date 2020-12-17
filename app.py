import argparse
import logging

from rich.logging import RichHandler

from config import Config
from flask_template import make_app


def _main():
    try:
        parsed_args = _parse_args()
        logger = logging.getLogger()
        logger.setLevel(logging.getLevelName(parsed_args.logging_level.upper()))
        logger.addHandler(RichHandler(rich_tracebacks=True))
        app, with_app_context_wraps = make_app(Config, False)
        app.run(
            host=app.config["APP_HOST"], port=app.config["APP_PORT"], debug=True, use_reloader=False
        )
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(e)
        raise


def _parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-ll", "--logging-level", type=str, default="info", help="logging level")
    parsed_args = parser.parse_args(args)
    return parsed_args


if __name__ == "__main__":
    _main()
