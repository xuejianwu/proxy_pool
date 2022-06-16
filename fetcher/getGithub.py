import requests, base64, json, time
from lxml import etree


def getRaw():

    for _ in range(3):
        try:
            # 爬虫获取最新代理数据
            ua = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",}
            rr = requests.get("https://github.com/freefq/free", headers=ua)

        except Exception as e:
            print("重试")
            time.sleep(3)
            continue
        break
    else:
        return []

    with open("page_source.html", 'w', encoding="utf-8") as f:
        f.write(rr.text)
    tree = etree.parse("page_source.html", etree.HTMLParser())
    r = tree.xpath("/html/body/div[4]/div/main/div[2]/div/div/div[3]/div[1]/readme-toc/div/div[2]/article/div/pre/code")
    proxyList = r[0].text.split("\n")
    # print(proxyList)

    # 解析代理数据
    result = []

    for proxy in proxyList:
        if "ss://" in proxy:
            # print(proxy)
            try:
                if "vmess://" in proxy:

                    # 1.解析成标准格式
                    _ = json.loads(str(base64.b64decode(proxy.split("//")[1]), encoding="utf-8"))
                    # print(f'{_}')

                    # 2.将标准格式解析成proxyPool接收的格式
                    vmess = {
                        "server": _["add"],
                        "port": _["port"],
                        "uuid": _["id"],
                        "alterId": _["aid"],
                        "cipher": _["type"],
                        "network": _["net"],
                        "ws-path": _["path"],
                        "type": "vmess"
                    }
                    # print(vmess)
                    result.append(vmess)

                else:
                    # 1.解析成标准格式
                    _ = proxy.split("//")[1].split("#")[0].split("@")
                    # print(f'{_}')
                    if len(_[0]) % 4 != 0:
                        for n in range(4-(len(_[0]) % 4)):
                            _[0] += "="
                    # print(len(_[0]))
                    # print(base64.b64decode(_[0]))
                    __ = str(base64.b64decode(_[0]), encoding="utf-8").split(":")

                    ss = {
                        "server": _[1].split(":")[0],
                        "port": _[1].split(":")[1],
                        "password": __[1],
                        "cipher": __[0],
                        "type": "ss"
                    }
                    # print(ss)
                    result.append(ss)

            except Exception as e:
                print(e)

    return result


if __name__ == "__main__":
    print(getRaw())