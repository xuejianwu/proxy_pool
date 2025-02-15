# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyApi.py
   Description :   WebApi
   Author :       JHao
   date：          2016/12/4
-------------------------------------------------
   Change Activity:
                   2016/12/04: WebApi
                   2019/08/14: 集成Gunicorn启动方式
                   2020/06/23: 新增pop接口
-------------------------------------------------
"""
__author__ = 'JHao'

import platform, json
from werkzeug.wrappers import Response
from flask import Flask, jsonify, request, abort

from util.six import iteritems
from util.EnDecrpty import encrypt
from helper.proxy import Proxy
from handler.proxyHandler import ProxyHandler
from handler.configHandler import ConfigHandler
from server2user.proxyMain import ProxyMain
from server2user.logout import logout


app = Flask(__name__)
conf = ConfigHandler()
proxy_handler = ProxyHandler()

# 启动代理管理器PM
proxyMain = ProxyMain()
# proxyMain.recheck()
# logout("proxyApi", f"ProxyMain()启动成功，并开始巡检")


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse

api_list = [
    {"url": "/get", "params": "type: ''https'|''", "desc": "get a proxy"},
    {"url": "/pop", "params": "", "desc": "get and delete a proxy"},
    {"url": "/delete", "params": "proxy: 'e.g. 127.0.0.1:8080'", "desc": "delete an unable proxy"},
    {"url": "/all", "params": "type: ''https'|''", "desc": "get all proxy from proxy pool"},
    {"url": "/count", "params": "", "desc": "return proxy count"}
    # 'refresh': 'refresh proxy pool',
]


def limit_remote_addr():
    """限制除信任ip地址意外的ip访问"""
    trustip = [
        "0.0.0.0",
        "127.0.0.1",
        "183.250.89.78"  # xuejw的d网机
    ]

    if request.remote_addr not in trustip:
        logout("limitIP", f"<拒绝>来自ip:<{request.remote_addr}>的请求")
        abort(403)
    logout("limitIP", f"<通过>来自ip:<{request.remote_addr}>的请求")


@app.route('/get/')
def get():
    https = request.args.get("type", "").lower() == 'https'
    proxy = proxy_handler.get(https)
    return encrypt(json.dumps(proxy.to_dict)) if proxy else {"code": 0, "src": "no proxy"}


@app.route('/get2clear/')
def get2clear():
    limit_remote_addr()
    https = request.args.get("type", "").lower() == 'https'
    proxy = proxy_handler.get(https)
    return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


# @app.route('/pop/')
# def pop():
#     https = request.args.get("type", "").lower() == 'https'
#     proxy = proxy_handler.pop(https)
#     return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


# @app.route('/refresh/')
# def refresh():
#     # refresh会有守护程序定时执行，由api直接调用性能较差，暂不使用
#     return 'success'


@app.route('/all/')
def getAll():
    limit_remote_addr()
    https = request.args.get("type", "").lower() == 'https'
    proxies = proxy_handler.getAll(https)
    return jsonify([_.to_dict for _ in proxies])


@app.route('/delete/', methods=['GET'])
def delete():
    limit_remote_addr()
    proxy = request.args.get('proxy')

    logout("proxyApi", f"delete数据模块接收--{proxy}")
    status = proxy_handler.delete(Proxy(proxy))
    return {"code": 0, "src": status}


@app.route('/count/')
def getCount():
    limit_remote_addr()
    status = proxy_handler.getCount()
    return status


# 请求-开启代理
@app.route('/proxyStart/')
def proxy_start():
    limit_remote_addr()
    # 1.获取可用代理参数
    # 2.启动代理
    # 3.成功后返回pid，IP以及端口号；不成功返回信息
    return proxyMain.startproxy()


# 请求-关闭代理
@app.route('/proxyClose/', methods=['GET'])
def proxy_close():
    limit_remote_addr()
    # 1.接收pid参数
    pid = request.args.get('pid')
    # 2.根据pid关闭对应代理进程
    # *3.返回结果
    return proxyMain.closeproxy(pid)


# 请求-情况当前在使用的所有代理
@app.route('/proxyClear/', methods=['GET'])
def proxyClear():
    limit_remote_addr()
    # 1.接收pid参数
    # 2.根据pid关闭对应代理进程
    # *3.返回结果
    return proxyMain.closeAll()


# 查看当前所有代理状态
@app.route('/proxieslist/')
def proxieslist():
    limit_remote_addr()
    # 1.获取可用代理参数
    # 2.启动代理
    # 3.成功后返回pid，IP以及端口号；不成功返回信息
    return proxyMain.pprint()


def runFlask():
    if platform.system() == "Windows":
        app.run(host=conf.serverHost, port=conf.serverPort)
    else:
        import gunicorn.app.base

        class StandaloneApplication(gunicorn.app.base.BaseApplication):

            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super(StandaloneApplication, self).__init__()

            def load_config(self):
                _config = dict([(key, value) for key, value in iteritems(self.options)
                                if key in self.cfg.settings and value is not None])
                for key, value in iteritems(_config):
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        _options = {
            'bind': '%s:%s' % (conf.serverHost, conf.serverPort),
            'workers': 4,
            'accesslog': '-',  # log to stdout
            'access_log_format': '%(h)s %(l)s %(t)s "%(r)s" %(s)s "%(a)s"'
        }
        StandaloneApplication(app, _options).run()


if __name__ == '__main__':
    runFlask()
