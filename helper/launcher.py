# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     launcher
   Description :   启动器
   Author :        JHao
   date：          2021/3/26
-------------------------------------------------
   Change Activity:
                   2021/3/26: 启动器
-------------------------------------------------
"""
__author__ = 'JHao'

import sys
from db.dbClient import DbClient
from handler.logHandler import LogHandler
from handler.configHandler import ConfigHandler

log = LogHandler('launcher')


def startServer():
    __beforeStart()
    from api.proxyApi import runFlask
    runFlask()


def startScheduler():
    __beforeStart()
    from helper.scheduler import runScheduler
    runScheduler()


def __beforeStart():
    __showVersion()
    __showConfigure()
    if __checkDBConfig():
        log.info('exit!')
        sys.exit()


def __showVersion():
    from setting import VERSION
    log.info("ProxyPool Version: %s" % VERSION)


def __showConfigure():
    conf = ConfigHandler()
    log.info("ProxyPool configure HOST: %s" % conf.serverHost)
    log.info("ProxyPool configure PORT: %s" % conf.serverPort)
    log.info("ProxyPool configure PROXY_FETCHER: %s" % conf.fetchers)


def __checkDBConfig():
    conf = ConfigHandler()
    db = DbClient(conf.dbConn)
    log.info("============ DATABASE CONFIGURE ================")
    log.info("DB_TYPE: %s" % db.db_type)
    log.info("DB_HOST: %s" % db.db_host)
    log.info("DB_PORT: %s" % db.db_port)
    log.info("DB_NAME: %s" % db.db_name)
    log.info("DB_USER: %s" % db.db_user)
    log.info("=================================================")
    return db.test()


# 采用简单的循环启动
def startScheduler2():
    __beforeStart()
    from fetcher.proxyFetcher import ProxyFetcher
    from setting import PROXY_FETCHER
    from server2user.logout import logout
    import time

    fetcher = ProxyFetcher()
    while True:
        for func in PROXY_FETCHER:
            try:
                f = getattr(fetcher, func, None)
                f()
            except Exception as e:
                logout("launcher", e)
        time.sleep(120)


def startRecheck():
    __beforeStart()
    from server2user.proxyRecheck import ProxyRecheck
    recheck = ProxyRecheck()
    recheck.run()
