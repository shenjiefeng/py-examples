# encoding: utf-8
__author__ = 'fengshenjie'

from random import randint
import requests
from bs4 import BeautifulSoup
import os
from util import timecount
from my_celery import mycelery

BID_LEN = 20
BID_LIST_LEN = 500
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
}


def gen_bids():
    bids = []
    for i in range(BID_LIST_LEN):
        bid = []
        for x in range(BID_LEN):
            bid.append(chr(randint(65, 90)))
        bids.append("".join(bid))
    return bids


def get_proxy_ip(fullfilename):
    with open(fullfilename) as fp:
        return [i.strip() for i in fp.readlines() if i is not '\n']


def write2file(txt, filename, path='./'):
    assert txt is not None
    if not os.access(path, os.W_OK):
        os.mkdir(path)
    with open(path + filename, 'w+', encoding='utf8') as fp:
        fp.write(str(txt))
        fp.write('\n')
    print(path + filename + ' updated.')


def verify_ips(ips, test_url='https://www.douban.com/'):
    '''
    vertify ip list
    :param ips: origin ip list
    :return: available ip list
    '''
    # test_url = 'https://httpbin.org/get'
    # test_url = 'https://www.baidu.com/'
    aval_ips = []
    ips = list(set(ips))
    for ip in ips:
        print('verify' + ip)
        proxies = {'http': 'http://' + ip,
                   'https': 'http://' + ip
                   }
        try:
            resp = requests.get(test_url, headers=header, proxies=proxies, timeout=5)
            if resp.status_code is 200 and resp.text:
                # print(resp.text)
                aval_ips.append(ip)
        except Exception as e:
            print('ip {} failed.'.format(ips.index(ip)))

    print('\navailable rate:', len(aval_ips) / len(ips) * 100, '%')
    return aval_ips


@timecount()
@mycelery.task
def update_ips(filename):
    # 1. 大量数据分步骤，先获取ip存起来，再验证
    # write2file('\n'.join(get_xicidaili_list()), filename)
    # ips = get_proxy_ip(filename)
    # 2. 少量数据
    ips = get_xicidaili_list()
    txt = '\n'.join(verify_ips(ips))
    write2file(txt, filename, path='/Users/fsj/github/py-examples/douban_group/util/')


def get_kuaidaili_list():
    url = "http://www.kuaidaili.com/proxylist/%s/"
    print('=> get:' + url)
    ips = []
    for i in range(1, 3):
        url = url % i
        resp = requests.get(url, headers=header)
        soup = BeautifulSoup(resp.text, 'html.parser')
        trs = soup.find_all('tbody')[2].find_all('tr')
        for tr in trs:
            if 'HTTPS' in tr.text:
                ip = tr.find('td', attrs={"data-title": "IP"})
                port = tr.find('td', attrs={"data-title": "PORT"})
                ips.append(ip.text + ':' + port.text)

    return ips


def get_xicidaili_list():
    url = 'http://www.xicidaili.com/wn/{}'
    print('=> get:' + url)
    ips = []
    for i in range(1, 2):
        resp = requests.get(url.format(i), headers=header, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tr in soup.find_all('tr', class_=True):
            ips.append(tr.find_all('td')[1].text + ':'
                       + tr.find_all('td')[2].text)

    return ips


if __name__ == '__main__':
    ''' https://github.com/hi-august/scrapy-learn/blob/master/get_proxy_ip.py '''
    name = 'ip.txt'
    update_ips(name)

'''
proxy eg:
verify 110.73.30.16:8123
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"
  }, 
  "origin": "110.73.30.16", 
  "url": "https://httpbin.org/get"
}
'''
