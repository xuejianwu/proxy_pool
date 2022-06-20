import requests
import re
import datetime
import json
import time
import random
import base64
from fetcher.getYesterday import getDatetimeYesterday
from server2user.logout import logout

result = []

def get1Cookie():
    """
    1.获取初始的cookie等信息
    :return: csrf, cookieSession
    """

    url = "https://vpnse.org/t/freenode"
    response = requests.get(url)
    header = response.headers
    csrf = header['X-CSRF-Token']
    cookieSession = header['Set-Cookie'].split("; ")[0][15:]
    logout("vpnse", f"初始cookie1：{csrf}")
    logout("vpnse", f"初始cookie2：{cookieSession}")
    return csrf, cookieSession


def getUrl():
    """
    2.获取有免费代理帖子的URL
    :return: [urls]
    """
    headers = {
        "authority": "vpnse.org",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Microsoft Edge\";v=\"102\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41"
    }
    cookies = {
        "_ga": "GA1.1.985391464.1652413400",
        "__gads": "ID=ef6594650bc7afb2-22f4dc382bd3001f:T=1652413434:RT=1652413434:S=ALNI_MZ4saGqIt-5ir9zUvNBgYiWRKDfZw",
        "__gpi": "UID=0000054bb9529234:T=1652413454:RT=1652413454:S=ALNI_MbfVN52fEi7hgXEjcHZaJBXt084rw",
        "flarum_remember": "ixzyi98q7gdImQ1QzQcyaBvMPaSvJIMnHK0ISebs",
        "_ga_8B2ENCJKBL": "GS1.1.1652413400.1.1.1652414086.0",
        "flarum_session": "dpj4bRNd2clvEOn1t08KVWZOMn6UKrXxNyGsE7nY"
    }
    url = "https://vpnse.org/t/freenode"
    rr = requests.get(url, headers=headers, cookies=cookies)

    temp = []
    pattern = re.compile(r'http[\S]+">', re.M)

    date = datetime.datetime.now().strftime("%Y,%m,%d").split(",")
    if len(date[1]) == 2:
        if date[1][0] == "0":
            date[1] = date[1][1]
    if len(date[2]) == 2:
        if date[2][0] == "0":
            date[2] = date[2][1]
    date = "-".join(date)

    for line in rr.text.split("/n"):
        m = pattern.findall(line)
        for url in m:
            if date in url or getDatetimeYesterday() in url:
            # if date in url:
                temp.append(url[:-2])

    logout("vpnse", f"获取到帖子urls：{temp}")
    return temp


def login(csrf, cookieSession):
    """
    3.登录获取登录状态的csrf以及cookie
    :param csrf:
    :param cookieSession:
    :return: csrf, cookieSession
    """
    headers = {
        "authority": "vpnse.org",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://vpnse.org",
        "referer": "https://vpnse.org",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "x-csrf-token": csrf
    }
    cookies = {
        "flarum_session": cookieSession
    }
    url = "https://vpnse.org/login"
    data = {
        "identification": "kgdp08u8@uuf.me",
        "password": "meiya@2020",
        "remember": False
    }
    data = json.dumps(data)
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    header = response.headers
    csrf = header['X-CSRF-Token']
    cookieSession = header['Set-Cookie'].split("; ")[0][15:]
    logout("vpnse", f"登录后cookie2：{csrf}")
    logout("vpnse", f"登录后cookie2：{cookieSession}")
    return csrf, cookieSession


def comment(csrf, cookieSession, p_url):
    """
    4.评论该帖子，再重新加载页面获取代理
    :param csrf:
    :param cookieSession:
    :param url:
    :param url_id: url.split("-")[0].split("/")[-1]
    :return:
    """
    headers = {
        "authority": "vpnse.org",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://vpnse.org",
        "referer": p_url,
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "x-csrf-token": csrf
    }
    cookies = {
        "flarum_session": cookieSession
    }
    url = "https://vpnse.org/api/posts"
    data = {
        "data": {
            "type": "posts",
            "attributes": {
                "content": "6666"
            },
            "relationships": {
                "discussion": {
                    "data": {
                        "type": "discussions",
                        "id": int(p_url.split("-")[0].split("/")[-1])
                    }
                }
            }
        }
    }
    data = json.dumps(data)
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    logout("vpnse", f"评论接口响应：{response.text}")
    logout("vpnse", f"评论接口响应：{response}")


def getProxyAfterLogin(cookieSession, p_url):
    headers = {
        "authority": "vpnse.org",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "referer": p_url,
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    cookies = {
        "flarum_session": cookieSession
    }
    url = p_url
    response = requests.get(url, headers=headers, cookies=cookies)

    pattern = re.compile(r'vmess://[\S]+<br>', re.M)

    for proxy in pattern.findall(response.text):
        logout("vpnse", f"原始数据：{proxy}")

        pp = proxy.replace("<em>", "").replace("</em>", "")
        pp = pp[:-4].split("://")[1].replace("-", "+").replace("_", "=")
        if len(pp) % 4 != 0:
            for n in range(4 - (len(pp) % 4)):
                pp += "="
        pp = pp.split("#")[0]
        logout("vpnse", f"base64解析前数据：{pp}")
        pp = json.loads(str(base64.b64decode(pp), encoding="utf-8"))
        logout("vpnse", f"base64解析后数据：{pp}")

        try:
            if "vmess://" in proxy:

                # 2.将标准格式解析成proxyPool接收的格式
                vmess = {
                    "server": pp["add"],
                    "port": pp["port"],
                    "uuid": pp["id"],
                    "alterId": pp["aid"],
                    "cipher": pp["scy"],
                    "network": pp["net"],
                    "ws-path": pp["path"],
                    "type": "vmess"
                }
                # if vmess["cipher"] == "none":
                #     vmess["cipher"] = "auto"
                if vmess["ws-path"] == "":
                    vmess["ws-path"] = "/"
                logout("vpnse", f"输出代理数据：{vmess}")
                result.append(vmess)

            else:
                # # 1.解析成标准格式
                # _ = proxy.split("//")[1].split("#")[0].split("@")
                # # logout("vpnse", f'{_}')
                # if len(_[0]) % 4 != 0:
                #     for n in range(4 - (len(_[0]) % 4)):
                #         _[0] += "="
                # # logout("vpnse", len(_[0]))
                # # logout("vpnse", base64.b64decode(_[0]))
                # __ = str(base64.b64decode(_[0]), encoding="utf-8").split(":")
                #
                # ss = {
                #     "server": _[1].split(":")[0],
                #     "port": _[1].split(":")[1],
                #     "password": __[1],
                #     "cipher": __[0],
                #     "type": "ss"
                # }
                # # logout("vpnse", ss)
                # result.append(ss)

                pass

        except Exception as e:
            logout("vpnse", f"vmess数据解析：{e}")


def getRaw():

    # 1.获取初始cookie
    c1, f1 = get1Cookie()
    # 2.获取目标帖子Url
    urls = getUrl()
    # 3.获取登录后的cookie
    c2, f2 = login(c1, f1)
    # 4.遍历目标帖子-先评论，再刷新爬取
    for url in urls:
        logout("vpnse", url)
        comment(c2, f2, url)
        time.sleep(random.randint(2, 4))
        getProxyAfterLogin(f2, url)
        time.sleep(random.randint(30, 40))  # 不休眠访问太快的话，只有第一个站点的评论成功，其余失败

    logout("vpnse", len(result), result)
    return result


if __name__ == '__main__':

    result = []

    # 1.获取初始cookie
    c1, f1 = get1Cookie()
    # 2.获取目标帖子Url
    urls = getUrl()
    # 3.获取登录后的cookie
    c2, f2 = login(c1, f1)
    # 4.遍历目标帖子-先评论，再刷新爬取
    for url in urls:
        logout("vpnse", url)
        comment(c2, f2, url)
        time.sleep(random.randint(2, 4))
        getProxyAfterLogin(f2, url)
        time.sleep(random.randint(10, 12))  # 不休眠访问太快的话，只有第一个站点的评论成功，其余失败

    logout("vpnse", len(result), result)

