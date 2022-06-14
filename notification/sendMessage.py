import json
import time
import requests
import hmac
import hashlib
import base64
import urllib.parse


def get_sign():
    """获取签名"""
    timestamp = str(round(time.time() * 1000))
    secret = 'SECd12e218321368978c68e28d7f2e989cc305fa1dd5bb9db5861e445da888c222c'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(timestamp)
    print(sign)
    return timestamp, sign


def send_dingding_message(message):
    """通过钉钉机器人发送预警消息"""

    timestamp, sign = get_sign()

    url = f"https://oapi.dingtalk.com/robot/send?access_token=1c2e1597d755aeffc941e9087de6f8f7896cb8a0ca64a659209ccdb4656f68c7&timestamp={timestamp}&sign={sign}"
    HEADERS = {
        "Content-Type": "application/json;charset=utf-8"
    }
    String_textMsg = {
        "msgtype": "markdown",
        "markdown":
            {
                "title": "测试ing",
                "text": message
            },
        "at": {
            "atMobiles": [
                "15606004194"
            ]
        }
    }

    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)
    return res.text


def get_proxylist():
    res = requests.get("http://117.25.130.72:50101/count/")
    print(res.text)


if __name__ == "__main__":
    # send_dingding_message("大家好")
    get_proxylist()