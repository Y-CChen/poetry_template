from datetime import datetime

import flask
from flask_template import __version__, util


def test_ecpay_payment(client, config):
    url = "{}/ecpay/payment/".format(config["APP_URL_PREFIX"])
    assert flask.url_for("flask_template.resources.ecpay._post_payment") == url
    data = {"total_amount": 10, "item_names": ["good1", "good2"]}
    response = client.post(url, json=data)
    html = response.get_data(as_text=True)
    assert html.startswith("<form")


def test_ecpay_logistic_cvs(client, config):
    url = "{}/ecpay/logistic/cvs/".format(config["APP_URL_PREFIX"])
    assert flask.url_for("flask_template.resources.ecpay._post_logistic_cvs") == url
    data = {
        "logistic_sub_type": "FAMILY",
        "goods_amount": 10,
        "collection_amount": 10,
        "is_collection": 1,
        "goods_name": "test",
        "receiver_name": "葉大雄",
        "receiver_phone": "",
        "receiver_cell_phone": "0911111111",
        "receiver_mail": "test@gmail.com",
        "receiver_store_id": "006598",
        "return_store_id": "006598",
    }
    response = client.post(url, json=data)
    json = response.get_json(force=True)
    assert json["RtnCode"] == "300"
