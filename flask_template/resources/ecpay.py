from datetime import datetime

import flask
from flask_template import ecpay_payment_sdk

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route("/order/", methods=["POST"])
def _post_order():
    json = flask.request.get_json(force=True)
    order_params = {
        "MerchantTradeNo": datetime.utcnow().strftime("T%Y%m%d%H%M%S"),  # String(20)
        "StoreID": "",  # String(20)
        "MerchantTradeDate": datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
        "PaymentType": "aio",
        "TotalAmount": json["total_amount"],
        "TradeDesc": json.get("trade_desc", "null"),  # String(200)
        "ItemName": "#".join(json.get("item_names", list())),  # String(400)
        "ReturnURL": "https://www.ecpay.com.tw/return_url.php",  # String(200)
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
    ecpay_payment = ecpay_payment_sdk.ECPayPaymentSdk(
        MerchantID="2000132", HashKey="5294y06JbISpM5x9", HashIV="v77hoKGq4kWxNNIS"
    )
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    order_params.update(extend_params_3)
    order_params.update(extend_params_4)
    final_order_params = ecpay_payment.create_order(order_params)
    action_url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"  # development
    # action_url = "https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5"  # production
    html = ecpay_payment.gen_html_post_form(action_url, final_order_params)
    return html
