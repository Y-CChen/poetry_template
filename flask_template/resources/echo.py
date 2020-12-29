import flask

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route("", methods=["POST"])
def _post():
    json = flask.request.get_json(force=True)
    return flask.jsonify(json)
