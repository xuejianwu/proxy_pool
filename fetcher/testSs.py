import json, subprocess, time, random
from server2user.logout import logout
from setting import testUrl, proxyTool_dir


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


def testSs(ip, port, password, cipher):
    """
    测试代理是否真实可用
    """
    try:
        # 接收当前要测的vmess代理参数
        ss_config = {
            'ip': ip,
            'port': int(port),
            'password': password,
            'cipher': cipher
        }

        # ss配置文件
        conf_dir = proxyTool_dir + "/tools/Shadowsocks-web/shadowsocks.json"

        # 读取congif
        with open(conf_dir, 'r+', encoding='utf-8') as conf:
            source = json.load(conf)
            # 修改代理配置信息
            source['local_port'] = 10800  # 测试用的监听端口
            source['server'] = ss_config['ip']
            source['server_port'] = ss_config['port']
            source['password'] = ss_config['password']
            source['method'] = ss_config['cipher']

        # 写入config
        with open(conf_dir, 'w+', encoding='utf-8') as conf:
            conf.write(json.dumps(source, indent=4, ensure_ascii=False))

        # 启动进程
        inst = "sslocal -c " + proxyTool_dir + "/tools/Shadowsocks-web/shadowsocks.json"
        proc_vmess_test = subprocess.Popen(inst.split(" "))
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
            logout("testSs", f"ss.get---- {e}")
        time.sleep(5)

        # 关闭进程
        logout("testSs", f'pid--{proc_vmess_test.pid}')
        subprocess.call(["kill", "-9", str(proc_vmess_test.pid)]) # linux用
        # subprocess.call(["taskkill", "-F", "/pid", str(proc_vmess_test.pid)])  # windows用

        # 根据情况返回结果
        if int(flag) == 200:
            logout("testSs", f"ss--{str(ip)}:{str(port)}--测试站点:{testurl} -- connecting successfully ...")
            return True
        else:
            logout("testSs", f"ss--{str(ip)}:{str(port)}--测试站点:{testurl} -- connecting fail !")
            return False

    except Exception as e:
        logout("testSs", f"testss解析模块ERROR-- {e}")
        return False


def testSs2(ip, port, password, cipher):
    """
    测试代理是否真实可用
    """
    try:
        # 接收当前要测的vmess代理参数
        ss_config = {
            'ip': ip,
            'port': int(port),
            'password': password,
            'cipher': cipher
        }

        # ss配置文件
        conf_dir = proxyTool_dir + "/tools/Shadowsocks/shadowsocks.json"

        # 读取congif
        with open(conf_dir, 'r+', encoding='utf-8') as conf:
            source = json.load(conf)
            # 修改代理配置信息
            source['local_port'] = 13960  # recheck测试用的监听端口
            source['server'] = ss_config['ip']
            source['server_port'] = ss_config['port']
            source['password'] = ss_config['password']
            source['method'] = ss_config['cipher']

        # 写入config
        with open(conf_dir, 'w+', encoding='utf-8') as conf:
            conf.write(json.dumps(source, indent=4, ensure_ascii=False))

        # 启动进程
        inst = "sslocal -c " + proxyTool_dir + "/tools/Shadowsocks/shadowsocks.json"
        proc_vmess_test = subprocess.Popen(inst.split(" "))
        time.sleep(6)

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
            logout("testSs2", f"ss.get---- {e}")

        # 关闭进程
        logout("testSs2", f'pid--{proc_vmess_test.pid}')
        subprocess.call(["kill", "-9", str(proc_vmess_test.pid)]) # linux用
        # subprocess.call(["taskkill", "-F", "/pid", str(proc_vmess_test.pid)])  # windows用
        time.sleep(5)

        # 根据情况返回结果
        if int(flag) == 200:
            logout("testSs2", f"ss--{str(ip)}:{str(port)}--测试站点:{testurl} -- connecting successfully ...")
            return True
        else:
            logout("testSs2", f"ss--{str(ip)}:{str(port)}--测试站点:{testurl} -- connecting fail !")
            return False

    except Exception as e:
        logout("testSs2", f"testss解析模块ERROR-- {e}")
        return False


def testSswin(ip, port, password, cipher):
    """
    测试代理是否真实可用
    """
    try:
        # 接收当前要测的vmess代理参数
        ss_config = {
            'ip': ip,
            'port': int(port),
            'password': password,
            'cipher': cipher
        }

        # ss配置文件
        conf_dir = "./tools/Shadowsocks-4.1/gui-config.json"

        # 读取congif
        with open(conf_dir, 'r+', encoding='utf-8') as conf:
            source = json.load(conf)
            # 修改代理配置信息
            source['local_port'] = 10800  # 测试用的监听端口
            source['server'] = ss_config['ip']
            source['server_port'] = ss_config['port']
            source['password'] = ss_config['password']
            source['method'] = ss_config['cipher']

        # 写入config
        with open(conf_dir, 'w+', encoding='utf-8') as conf:
            conf.write(json.dumps(source, indent=4, ensure_ascii=False))

        # 启动进程
        proc_vmess_test = subprocess.Popen("F:\\Document\\proxy_pool_linux\\tools\\Shadowsocks-4.1\\Shadowsocks.exe")
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
            logout("testSs", f"ss.get---- {e}")
        time.sleep(5)

        # 关闭进程
        logout("testSs", f'pid--{proc_vmess_test.pid}')
        # subprocess.call(["kill", "-9", str(proc_vmess_test.pid)]) # linux用
        subprocess.call(["taskkill", "-F", "/pid", str(proc_vmess_test.pid)])  # windows用

        # 根据情况返回结果
        if int(flag) == 200:
            logout("testSs", f"ss--{str(ip)}:{str(port)}--测试站点:{testurl} -- connecting successfully ...")
            return True
        else:
            logout("testSs", f"ss--{str(ip)}:{str(port)}--测试站点:{testurl} -- connecting fail !")
            return False

    except Exception as e:
        logout("testSs", f"testss解析模块ERROR-- {e}")
        return False


def tests():
    # 测试可用性
    import requests
    flag = False
    testurl = random.choice(testUrl)
    try:
        proxy = {"http": "socks5h://127.0.0.1:10800", "https": "socks5h://127.0.0.1:10800"}

        session = requests.Session()
        session.trust_env = False

        response = session.get(testurl, proxies=proxy, )
        flag = response.status_code

    except Exception as e:
        logout("testSs", f"ss.get---- {e}")
    time.sleep(5)

    # 根据情况返回结果
    if int(flag) == 200:
        logout("testSs", f"ss----测试站点:{testurl} -- connecting successfully ...")
        return True
    else:
        logout("testSs", f"ss----测试站点:{testurl} -- connecting fail !")
        return False


if __name__ == '__main__':
    testSs2("150.230.96.106", "57239")