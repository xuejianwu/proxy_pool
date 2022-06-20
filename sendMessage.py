import json
import time
import requests
import hmac
import hashlib
import base64
import urllib.parse
import click
from server2user import logout


@click.group()
@click.version_option()
def cli():
    """My Cli"""


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
        "msgtype": "text",
        "text":
            {
                "content": message
            }
        }

    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)
    return res.text


def send_dingding_message_at(message):
    """通过钉钉机器人发送预警消息+@"""

    timestamp, sign = get_sign()

    url = f"https://oapi.dingtalk.com/robot/send?access_token=1c2e1597d755aeffc941e9087de6f8f7896cb8a0ca64a659209ccdb4656f68c7&timestamp={timestamp}&sign={sign}"
    HEADERS = {
        "Content-Type": "application/json;charset=utf-8"
    }
    String_textMsg = {
        "msgtype": "text",
        "text":
            {
                "content": message
            },
        "at": {
            "atMobiles": ["15606004194"],
        }
    }

    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)
    return res.text


def get_proxylist():
    # 当前可用
    url1 = "http://127.0.0.1:50101/proxieslist"
    # 库里所有
    url2 = "http://127.0.0.1:50101/count"

    res1 = requests.get(url1).text  # usingTable-0-{}
                                    # validTable-id-140335087807936-8-['{"server": "cdn-cn.nekocloud.cn", "port": "19079", "uuid": "76cb50a4-9fd8-352e-99f4-a7bb5959b07b", "alterId": "0", "cipher": "auto", "network": "ws", "ws-path": "/dahjwuh", "protocol": "vmess"}', '{"server": "51.81.223.32", "port": "443", "uuid": "c0156451-4efb-45e2-84fc-8d315c4650db", "alterId": "32", "cipher": "auto", "network": "tcp", "ws-path": "/", "protocol": "vmess"}', '{"server": "51.81.223.10", "port": "443", "uuid": "c0156451-4efb-45e2-84fc-8d315c4650db", "alterId": "32", "cipher": "auto", "network": "tcp", "ws-path": "/", "protocol": "vmess"}', '{"server": "51.81.223.20", "port": "443", "uuid": "c0156451-4efb-45e2-84fc-8d315c4650db", "alterId": "32", "cipher": "auto", "network": "tcp", "ws-path": "/", "protocol": "vmess", "listenport": 33454}', '{"server": "51.81.223.29", "port": "443", "uuid": "c0156451-4efb-45e2-84fc-8d315c4650db", "alterId": "32", "cipher": "auto", "network": "tcp", "ws-path": "/", "protocol": "vmess", "listenport": 42739}', '{"server": "cdn-cn.nekocloud.cn", "port": "19047", "uuid": "76cb50a4-9fd8-352e-99f4-a7bb5959b07b", "alterId": "0", "cipher": "auto", "network": "ws", "ws-path": "/dahjwuh", "protocol": "vmess"}', '{"server": "51.81.223.17", "port": "443", "uuid": "c0156451-4efb-45e2-84fc-8d315c4650db", "alterId": "32", "cipher": "auto", "network": "tcp", "ws-path": "/", "protocol": "vmess"}', '{"server": "cdn-cn.nekocloud.cn", "port": "19049", "uuid": "76cb50a4-9fd8-352e-99f4-a7bb5959b07b", "alterId": "0", "cipher": "auto", "network": "ws", "ws-path": "/dahjwuh", "protocol": "vmess"}']
                                    # unvalidTable-id-140335088231360-0-[]
                                    # listenportTable-0-[]
    res2 = requests.get(url2).text  # {"count":{"https":0,"total":4}}

    res1 = res1.split("\n")
    using = res1[0].split("-")[1]
    used = res1[1].split("-")[3]
    datebase = json.loads(res2)["count"]["total"]

    return int(using), int(used), int(datebase)


@cli.command(name="Hour")
def checkByHour():
    using, used, datebase = get_proxylist()
    if using+used == 0:
        message = f"【yao2代理预警】-当前无可用代理"
        logout.logout("dding", message)
        send_dingding_message_at(message)
    elif using+used < 50:
        message = f"【yao2代理预警】-当前可用代理数量为：<{using+used}>"
        logout.logout("dding", message)
        send_dingding_message_at(message)
    else:
        message = f"【yao2代理预警】-当前可用代理数量为：<{using + used}>"
        logout.logout("dding", message)
        send_dingding_message(message)


@cli.command(name="Day")
def checkByDay():
    using, used, datebase = get_proxylist()
    if using+used < 50:
        message = f"【yao2代理信息播报】-当前可用代理数量为：<{using+used}>"
        logout.logout("dding", message)
        send_dingding_message(message)
    else:
        message = f"【yao2代理信息播报】-当前可用代理数量为：<{using + used}>"
        logout.logout("dding", message)
        send_dingding_message(message)


if __name__ == "__main__":
    cli()
