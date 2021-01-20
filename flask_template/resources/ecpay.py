from datetime import datetime

import flask
from flask_template import ecpay_logistic_sdk, ecpay_payment_sdk

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route("/payment/", methods=["POST"])
def _post_payment():
    json = flask.request.get_json(force=True)
    order_params = {
        "MerchantTradeNo": datetime.utcnow().strftime("T%Y%m%d%H%M%S"),  # String(20)
        "StoreID": "",  # String(20)
        "MerchantTradeDate": datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
        "PaymentType": "aio",
        "TotalAmount": json["total_amount"],
        "TradeDesc": json.get("trade_desc", "null"),  # String(200)
        "ItemName": "#".join(json.get("item_names", list())),  # String(400)
        "ReturnURL": "{}{}".format(
            flask.current_app.config["NGROK_URL"],
            flask.url_for("flask_template.resources.ecpay._post_payment_return"),
        ),  # String(200)
        "ChoosePayment": "ALL",
        "ClientBackURL": json.get("client_back_url", ""),  # String(200)
        "ItemURL": "https://www.ecpay.com.tw/item_url.php",  # String(200)
        "Remark": json.get("remark", ""),  # String(100)
        "ChooseSubPayment": "",
        "OrderResultURL": "",  # String(200)
        "NeedExtraPaidInfo": "Y",
        "DeviceSource": "",
        "IgnorePayment": "",
        "PlatformID": "",
        "InvoiceMark": "N",
        "CustomField1": "",
        "CustomField2": "",
        "CustomField3": "",
        "CustomField4": "",
        "EncryptType": 1,
    }
    extend_params_1 = {
        "ExpireDate": 7,
        "PaymentInfoURL": "https://www.ecpay.com.tw/payment_info_url.php",
        "ClientRedirectURL": "",
    }
    extend_params_2 = {
        "StoreExpireDate": 15,
        "Desc_1": "",
        "Desc_2": "",
        "Desc_3": "",
        "Desc_4": "",
        "PaymentInfoURL": "https://www.ecpay.com.tw/payment_info_url.php",
        "ClientRedirectURL": "",
    }
    extend_params_3 = {
        "BindingCard": 0,
        "MerchantMemberID": "",
    }
    extend_params_4 = {
        "Redeem": "N",
        "UnionPay": 0,
    }
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    order_params.update(extend_params_3)
    order_params.update(extend_params_4)
    ecpay_payment = ecpay_payment_sdk.ECPayPaymentSdk(
        MerchantID=flask.current_app.config["ECPAY_MERCHANT_ID"],
        HashKey=flask.current_app.config["ECPAY_HASH_KEY"],
        HashIV=flask.current_app.config["ECPAY_HASH_IV"],
    )
    final_order_params = ecpay_payment.create_order(order_params)
    action_url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"  # development
    # action_url = "https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5"  # production
    html = ecpay_payment.gen_html_post_form(action_url, final_order_params)
    return html

@blueprint.route("/payment/return/", methods=["POST"])
def _post_payment_return():
    ecpay_payment = ecpay_payment_sdk.ECPayPaymentSdk(
        MerchantID=flask.current_app.config["ECPAY_MERCHANT_ID"],
        HashKey=flask.current_app.config["ECPAY_HASH_KEY"],
        HashIV=flask.current_app.config["ECPAY_HASH_IV"],
    )
    check_mac_value = ecpay_payment.generate_check_value(flask.request.form.to_dict())
    if flask.request.form["CheckMacValue"] != check_mac_value:
        return "|FAIL"
    return "1|OK"


@blueprint.route("/logistic/cvs/", methods=["POST"])
def _post_logistic_cvs():
    json = flask.request.get_json(force=True)
    order_params = {
        "MerchantTradeNo": datetime.utcnow().strftime("T%Y%m%d%H%M%S"),  # String(20)
        "MerchantTradeDate": datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
        "LogisticsType": ecpay_logistic_sdk.LogisticsType["CVS"],
        "LogisticsSubType": ecpay_logistic_sdk.LogisticsSubType[json["logistic_sub_type"]],
        "GoodsAmount": json["goods_amount"],
        "CollectionAmount": json.get("collection_amount", 0),
        "IsCollection": ecpay_logistic_sdk.IsCollection[
            "YES" if json.get("is_collection", 0) == 1 else "NO"
        ],
        "GoodsName": json["goods_name"],  # String(50)
        "SenderName": "測試寄件者",  # String(10)
        "SenderPhone": "0226550115",
        "SenderCellPhone": "0911222333",
        "ReceiverName": json["receiver_name"],  # String(10)
        "ReceiverPhone": json["receiver_phone"],
        "ReceiverCellPhone": json["receiver_cell_phone"],
        "ReceiverEmail": json["receiver_mail"],  # String(50)
        "TradeDesc": json.get("trade_desc", "null"),  # String(200)
        "ServerReplyURL": "{}{}".format(
            flask.current_app.config["NGROK_URL"],
            flask.url_for("flask_template.resources.ecpay._post_logistic_cvs_server_reply"),
        ),  # String(200)
        "ClientReplyURL": json.get("client_reply_url", ""),  # String(200)
        "Remark": json.get("remark", ""),  # String(200)
        "PlatformID": "",
        "LogisticsC2CReplyURL": "https://www.ecpay.com.tw/logistics_c2c_reply",  # String(200)
    }
    shipping_cvs_params = {
        "ReceiverStoreID": json["receiver_store_id"],
        "ReturnStoreID": json["return_store_id"],
    }
    order_params.update(shipping_cvs_params)
    ecpay_logistic = ecpay_logistic_sdk.ECPayLogisticSdk(
        MerchantID=flask.current_app.config["ECPAY_MERCHANT_ID"],
        HashKey=flask.current_app.config["ECPAY_HASH_KEY"],
        HashIV=flask.current_app.config["ECPAY_HASH_IV"],
    )
    action_url = "https://logistics-stage.ecpay.com.tw/Express/Create"  # development
    # action_url = "https://logistics.ecpay.com.tw/Express/Create"  # production
    shipping_order = ecpay_logistic.create_shipping_order(
        action_url=action_url, client_parameters=order_params
    )
    return flask.jsonify(shipping_order), 201


@blueprint.route("/logistic/cvs/server_reply/", methods=["POST"])
def _post_logistic_cvs_server_reply():
    ecpay_logistic = ecpay_logistic_sdk.ECPayLogisticSdk(
        MerchantID=flask.current_app.config["ECPAY_MERCHANT_ID"],
        HashKey=flask.current_app.config["ECPAY_HASH_KEY"],
        HashIV=flask.current_app.config["ECPAY_HASH_IV"],
    )
    check_mac_value = ecpay_logistic.generate_check_value(flask.request.form.to_dict())
    if flask.request.form["CheckMacValue"] != check_mac_value:
        return "|FAIL"
    return "1|OK"
