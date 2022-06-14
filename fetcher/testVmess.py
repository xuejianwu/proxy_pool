import re, json, os, subprocess, time, random
from server2user.logout import logout
from setting import testUrl, proxyTool_dir


def testVmess(ip, port, uuid, alterId, cipher, network, ws_path):
    """
    测试代理是否真实可用
    """
    try:
        # 接收当前要测的vmess代理参数
        vmess_config = {
            'ip': ip,
            'port': int(port),
            'uuid': uuid,
            'alterId': int(alterId),
            'cipher': cipher,
            'network': network,
            'ws_path': ws_path
        }

        # v2ray配置文件
        conf_dir = proxyTool_dir + "/tools/v2ray-cli-web/config.json"

        # 读取congif
        with open(conf_dir, 'r+', encoding='utf-8') as conf:
            source = json.load(conf)
            # 修改代理配置信息
            source['inbounds'][0]['port'] = 10800  # 测试用的监听端口
            source['outbounds'][0]['settings']['vnext'][0] = {
                "address": vmess_config['ip'],
                "port": vmess_config['port'],
                "users": [
                    {
                    "id": vmess_config['uuid'],
                    "alterId": vmess_config['alterId'],
                    "email": "t@t.tt",
                    "security": vmess_config['cipher']
                    }
                ]
                }
            source['outbounds'][0]['streamSettings'] = {
                "network": vmess_config['network'],
                "wsSettings": {
                    "path": vmess_config['ws_path']
                }
            }
            if vmess_config['ws_path'] is None:
                source['outbounds'][0]['streamSettings'].pop('ws_path')

        # 写入config
        with open(conf_dir, 'w+', encoding='utf-8') as conf:
            conf.write(json.dumps(source, indent=4, ensure_ascii=False))

        # 启动进程
        proc_vmess_test = subprocess.Popen(proxyTool_dir + "/tools/v2ray-cli-web/v2ray")
        time.sleep(3)

        # 测试可用性
        import requests
        flag = False
        testurl = random.choice(testUrl)
        try:
            proxy = {"http": "socks5h://127.0.0.1:10800", "https": "socks5h://127.0.0.1:10800"}

            session = requests.Session()
            session.trust_env = False

            response = session.get(testurl, proxies=proxy, headers=get_request_headers(), timeout=10)
            flag = response.status_code

        except Exception as e:
            logout("testVmess", f"v2ray.get---- {e}")
        time.sleep(5)

        # 关闭进程
        logout("testVmess", f'pid--{proc_vmess_test.pid}')
        subprocess.call(["kill", "-9", str(proc_vmess_test.pid)])

        # 根据情况返回结果
        if int(flag) == 200:
            logout("testVmess", f"v2ray--{str(ip)}:{str(port)}-- connecting successfully ...")
            return True
        else:
            logout("testVmess", f"v2ray--{str(ip)}:{str(port)}-- connecting fail !")
            return False

    except Exception as e:
        logout("testVmess", f"testVmess解析模块ERROR-- {e}")
        return False


def testVmess2(ip, port, uuid, alterId, cipher, network, ws_path):
    """
    测试代理是否真实可用
    """
    try:
        # 接收当前要测的vmess代理参数
        vmess_config = {
            'ip': ip,
            'port': int(port),
            'uuid': uuid,
            'alterId': int(alterId),
            'cipher': cipher,
            'network': network,
            'ws_path': ws_path
        }

        # v2ray配置文件
        conf_dir = proxyTool_dir + "/tools/v2ray-cli/config.json"

        # 读取congif
        with open(conf_dir, 'r+', encoding='utf-8') as conf:
            source = json.load(conf)
            # 修改代理配置信息
            source['inbounds'][0]['port'] = 13960  # 测试用的监听端口
            source['outbounds'][0]['settings']['vnext'][0] = {
                "address": vmess_config['ip'],
                "port": vmess_config['port'],
                "users": [
                    {
                        "id": vmess_config['uuid'],
                        "alterId": vmess_config['alterId'],
                        "email": "t@t.tt",
                        "security": vmess_config['cipher']
                    }
                ]
            }
            source['outbounds'][0]['streamSettings'] = {
                "network": vmess_config['network'],
                "wsSettings": {
                    "path": vmess_config['ws_path']
                }
            }
            if vmess_config['ws_path'] is None:
                source['outbounds'][0]['streamSettings'].pop('ws_path')

        # 写入config
        with open(conf_dir, 'w+', encoding='utf-8') as conf:
            conf.write(json.dumps(source, indent=4, ensure_ascii=False))

        # 启动进程
        proc_vmess_test = subprocess.Popen(proxyTool_dir + "/tools/v2ray-cli/v2ray")
        time.sleep(3)

        # 测试可用性
        import requests
        flag = False
        testurl = random.choice(testUrl)
        try:
            proxy = {"http": "socks5h://127.0.0.1:13960", "https": "socks5h://127.0.0.1:13960"}

            session = requests.Session()
            session.trust_env = False

            response = session.get(testurl, proxies=proxy, headers=get_request_headers(), timeout=10)
            flag = response.status_code

        except Exception as e:
            logout("testVmess2", f"v2ray.get---- {e}")
        time.sleep(5)

        # 关闭进程
        logout("testVmess2", f'pid--{proc_vmess_test.pid}')
        subprocess.call(["kill", "-9", str(proc_vmess_test.pid)])

        # 根据情况返回结果
        if int(flag) == 200:
            logout("testVmess2", f"v2ray--{str(ip)}:{str(port)}-- connecting successfully ...")
            return True
        else:
            logout("testVmess2", f"v2ray--{str(ip)}:{str(port)}-- connecting fail !")
            return False

    except Exception as e:
        logout("testVmess2", f"testVmess解析模块ERROR-- {e}")
        return False


def get_request_headers():
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.4; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (X11; Linux i686; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.4; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (X11; Linux i686; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"
    ]

    headers = {

    'User-Agent': random.choice(USER_AGENTS)

    }

    return headers


def backup_testVmess(ip, port, uuid, alterId, cipher, network, ws_path):
    """
    测试代理是否真实可用
    """
    try:
        # 接收当前要测的vmess代理参数
        vmess_config = {
            'ip': ip,
            'port': int(port),
            'uuid': uuid,
            'alterId': int(alterId),
            'cipher': cipher,
            'network': network,
            'ws_path': ws_path
        }

        # v2ray配置文件
        conf_dir = proxyTool_dir + "/tools/v2ray-cli/config.json"

        # 读取congif
        with open(conf_dir, 'r+', encoding='utf-8') as conf:
            source = json.load(conf)
            # 修改代理配置信息
            source['inbounds'][0]['port'] = 10800  # 测试用的监听端口
            source['outbounds'][0]['settings']['vnext'][0] = {
                "address": vmess_config['ip'],
                "port": vmess_config['port'],
                "users": [
                    {
                    "id": vmess_config['uuid'],
                    "alterId": vmess_config['alterId'],
                    "email": "t@t.tt",
                    "security": vmess_config['cipher']
                    }
                ]
                }
            source['outbounds'][0]['streamSettings'] = {
                "network": vmess_config['network'],
                "wsSettings": {
                    "path": vmess_config['ws_path']
                }
            }
            if vmess_config['ws_path'] is None:
                source['outbounds'][0]['streamSettings'].pop('ws_path')

        # 写入config
        with open(conf_dir, 'w+', encoding='utf-8') as conf:
            conf.write(json.dumps(source, indent=4, ensure_ascii=False))

        # 启动进程
        proc_vmess_test = subprocess.Popen(proxyTool_dir + "/tools/v2ray-cli/v2ray")
        time.sleep(3)

        # 测试可用性
        import requests, socket, socks
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10800)
        socket.socket = socks.socksocket
        flag = False
        try:
            flag = requests.get(random.choice(testUrl), timeout=5).status_code
        except Exception as e:
            logout("testVmess", f"v2ray.get--{str(ip)}:{str(port)}-- {e}")
        time.sleep(5)

        # 关闭进程
        logout("testVmess", f'pid--{proc_vmess_test.pid}')
        subprocess.call(["kill", "-9", str(proc_vmess_test.pid)])

        # 关闭全局代理到10800
        socks.set_default_proxy()
        socket.socket = socks.socksocket

        # 根据情况返回结果
        if int(flag) == 200:
            logout("testVmess", f"v2ray--{str(ip)}:{str(port)}-- connecting successfully ...")
            return True
        else:
            logout("testVmess", f"v2ray--{str(ip)}:{str(port)}-- connecting fail !")
            return False

    except Exception as e:
        logout("testVmess", f"testVmess解析模块ERROR-- {e}")
        return False