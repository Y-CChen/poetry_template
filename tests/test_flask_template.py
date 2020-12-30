from datetime import datetime

import flask
from flask_template import __version__, util


def test_version():
    assert __version__ == "0.1.0"


def test_root(client):
    url = "/"
    assert flask.url_for("flask_template.resources.root._get") == url
    response = client.get(url)
    json = response.get_json(force=True)
    assert json["msg"] == "hello"
    assert util.isoformat_to_datetime(json["timestamp"])

def test_sitemap(client, config):
    url = "{}/".format(config["APP_URL_PREFIX"])
    assert flask.url_for("flask_template.resources.sitemap._get") == url


def test_echo(client, config):
    url = "{}/echo".format(config["APP_URL_PREFIX"])
    assert flask.url_for("flask_template.resources.echo._post") == url
    data = {"timestamp": datetime.utcnow().isoformat(timespec="seconds")}
    response = client.post(url, json=data)
    json = response.get_json(force=True)
    assert json == data
