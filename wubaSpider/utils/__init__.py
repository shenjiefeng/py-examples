from conf import UserAgent_List
import random
import traceback
import time

def getHeader1():
    '''
    精简版header
    ref: https://jim-bin.github.io/2017/03/04/python%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%9658%E5%90%8C%E5%9F%8E%E7%A7%9F%E6%88%BF%E4%BF%A1%E6%81%AF/
    :return:
    '''
    headers = {'User-Agent': random.choice(UserAgent_List),
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               'Accept-Encoding': 'gzip',
               }
    return headers