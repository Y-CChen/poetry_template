from datetime import datetime

import flask

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route("/", methods=["GET"])
def _get():
    return flask.jsonify(
        {"timestamp": datetime.utcnow().isoformat(timespec="seconds"), "msg": "hello"}
    )
