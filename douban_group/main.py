# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import re, random
import conf
import util, util.web
from util.log import logger


def getHeader():
    headerrow = random.choice(conf.raw_headers)
    res = {}
    lines = headerrow.split('\n')
    for line in lines:
        try:
            k, v = line.split(':')
            res[k] = v
        except Exception as e:
            print(e)
            print(line)
    return res


def getHeader2():
    return {
        "User-Agent": 'Baiduspider',
        'Cookie': 'bid="%s"' % random.choice(util.web.gen_bids()),
        'Accept-Language': "zh-CN,zh",
        'Referer': 'https://www.douban.com'
    }


def downloader(url):
    headers = getHeader2()
    ip = random.choice(util.web.get_proxy_ip('./util/ip.txt'))
    proxies = {'http': 'http://' + ip,
               'https': 'http://' + ip
               }
    logger.info('GET:' + url)
    logger.info('proxies ' + ip)
    # time.sleep(random.choice([1,2,1.5]))
    try:
        resp = requests.get(url, headers=headers, allow_redirects=False,
                            proxies=proxies, timeout=5)
        if 200 == resp.status_code:
            return resp.text
        else:
            raise Exception('{} found.'.format(resp.status_code))
    except Exception as e:
        logger.info(e)
        return ''


def parser(disscuss_url, keyword):
    text = downloader(disscuss_url)
    res = []
    if '' == text:
        return res
    soup = BeautifulSoup(text, "html.parser")
    tbl = soup.find_all('table')[1]
    links = tbl.find_all(name='a', href=re.compile('group/'))
    for a in links:
        title, url = a.attrs['title'], a.attrs['href']
        if parse_article(url, keyword):
            # yield title, url
            res.append((title, url))
    return res


def parse_article(url, keyword):
    text = downloader(url)
    if '' == text:
        return False
    soup = BeautifulSoup(text, 'html.parser')
    article = soup.find(name='div', class_='article')
    # 比re.match/search or str.find更快
    return keyword in article.text


@util.timecount(True)
@util.except_hander
def main():
    summary = []
    for i in range(3):
        url = 'https://www.douban.com/group/576564/discussion?start=' + str(i * 25)
        j = 0
        for t, u in parser(url, conf.KEYWORD):
            article = '{} {} {}'.format(j, t, u)
            logger.info(article)
            summary.append(article)
            j += 1
        if j == 0:
            logger.info('no result.')
    print()
    print(summary)


if __name__ == '__main__':
    main()
