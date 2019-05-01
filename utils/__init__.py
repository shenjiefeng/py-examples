# encoding: utf-8
__author__ = 'fengshenjie'
from utils.conf import UserAgentList
import random
import time
import traceback
import requests


def GetHeaderV1():
    headers = {'User-Agent': random.choice(UserAgentList),
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               'Accept-Encoding': 'gzip',
               }
    return headers


def Downloader(url, headers, encoding='utf8'):
    r = requests.get(url, headers=headers)
    r.encoding = encoding
    if not r.text:
        print('response text empty!')
    return r.text


def Timecount(funcname=''):
    '''带返回值'''

    def timecount_hander(func):
        def wrapper(*args, **kwargs):
            if funcname:
                name = funcname
            else:
                name = func
            timeStart = time.time()
            print(time.strftime('%H:%M:%S'), '{} start'.format(name))
            res = func(*args, **kwargs)
            timeEnd = time.time()
            print(time.strftime('%H:%M:%S'), '{} Time elapsed: {}'.format(name, timeEnd - timeStart))
            return res

        return wrapper

    return timecount_hander


def ErrHander(funcname=''):
    def fsjhandler(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                traceback.print_exc()
                # sendmail

        return wrapper

    return fsjhandler
