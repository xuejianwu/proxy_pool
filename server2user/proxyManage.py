import requests, json, time, subprocess, random
from setting import testUrl, proxyTool_dir
from server2user.logout import logout


class ProxyManager:
    """
    代理管理器，负责该服务与用户交互
    """
    def startproxy_vmess(self, ip, port, uuid, alterId, cipher, network, ws_path, listenport):
        """
        开启一个代理
        :param proxy: vmess代理参数
        :return: success-{pid}; fail-None
        """

        """
        测试代理是否真实可用
        """
        pid = ""
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
                source['inbounds'][0]['port'] = int(listenport)  # 测试用的监听端口
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
            pid = proc_vmess_test.pid
            time.sleep(3)

            # 测试可用性
            import requests
            flag = False
            testurl = random.choice(testUrl)

            try:
                proxy = {"http": f"socks5h://127.0.0.1:{listenport}", "https": f"socks5h://127.0.0.1:{listenport}"}

                session = requests.Session()
                session.trust_env = False

                response = session.get(testurl, proxies=proxy, headers=get_request_headers(), timeout=10)
                flag = response.status_code

            except Exception as e:
                logout("proxyManage", f"v2ray-requests.get-ERROR--{str(ip)}:{str(port)}--{listenport}-- {e}")
                return False, None

            time.sleep(5)

            if int(flag) == 200:
                logout("proxyManage", f"v2ray.get--{str(ip)}:{str(port)}--{listenport}-SUCCESSFUL")
                return True, pid

        except Exception as e:
            logout("proxyManage", f"v2ray.get-ERROR--{str(ip)}:{str(port)}--{listenport}-- {e}")
            # 关闭进程
            logout("proxyManage", f'pid--{pid}')
            subprocess.call(["kill", "-9", str(pid)])
            time.sleep(3)

    def startproxy_ss(self, ip, port, password, cipher, listenport):
        """
        开启一个代理
        :param proxy: ss代理参数
        :return: success-{pid}; fail-None
        """

        """
        测试代理是否真实可用
        """
        pid = ""
        try:
            # 接收当前要测的vmess代理参数
            ss_config = {
                'ip': ip,
                'port': int(port),
                'password': password,
                'cipher': cipher
            }

            # v2ray配置文件
            conf_dir = proxyTool_dir + "/tools/Shadowsocks/shadowsocks.json"

            # 读取congif
            with open(conf_dir, 'r+', encoding='utf-8') as conf:
                source = json.load(conf)
                # 修改代理配置信息
                source['local_port'] = int(listenport)  # 测试用的监听端口
                source['server'] = ss_config['ip']
                source['server_port'] = ss_config['port']
                source['password'] = ss_config['password']
                source['method'] = ss_config['cipher']

            # 写入config
            with open(conf_dir, 'w+', encoding='utf-8') as conf:
                conf.write(json.dumps(source, indent=4, ensure_ascii=False))

            # 启动进程
            inst = "sslocal -c " + proxyTool_dir + "/tools/Shadowsocks/shadowsocks.json"
            proc_ss_test = subprocess.Popen(inst.split(" "))
            pid = proc_ss_test.pid
            time.sleep(3)

            # 测试可用性
            import requests
            flag = False
            testurl = random.choice(testUrl)

            try:
                proxy = {"http": f"socks5h://127.0.0.1:{listenport}", "https": f"socks5h://127.0.0.1:{listenport}"}

                session = requests.Session()
                session.trust_env = False

                response = session.get(testurl, proxies=proxy, headers=get_request_headers(), timeout=10)
                flag = response.status_code

            except Exception as e:
                logout("proxyManage", f"ss-requests.get-ERROR--{str(ip)}:{str(port)}--{listenport}-- {e}")
                return False, None

            time.sleep(5)

            if int(flag) == 200:
                logout("proxyManage", f"ss.get--{str(ip)}:{str(port)}--{listenport}-SUCCESSFUL")
                return True, pid

        except Exception as e:
            logout("proxyManage", f"ss.get-ERROR--{str(ip)}:{str(port)}--{listenport}-- {e}")
            # 关闭进程
            logout("proxyManage", f'pid--{pid}')
            subprocess.call(["kill", "-9", str(pid)])
            time.sleep(3)

    def closeproxy(self, pid):
        """
        根据pid关闭一个代理
        :param pid: 代理进程id
        :return: True or False
        """
        try:
            subprocess.call(["kill", "-9", str(pid)])
            time.sleep(5)
            return True
        except Exception as e:
            logout("proxyManage", f"closeProxy--{e}")
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

    'User-Agent': random.choice(USER_AGENTS),

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

    'Accept-Language': 'en-US,en;q=0.5',

    'Connection': 'keep-alive',

    }

    return headers
