from operator import itemgetter

import flask

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route("/", methods=["GET"])
def _get():
    rules = sorted(
        (
            {
                "endpoint": rule.endpoint,
                "methods": ",".join(sorted(rule.methods)),
                "api": str(rule),
            }
            for rule in flask.current_app.url_map.iter_rules()
        ),
        key=itemgetter("api"),
    )
    return flask.jsonify(rules)
