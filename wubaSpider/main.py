# encoding: utf-8
__author__ = 'fengshenjie'
from utils import getHeader1
from utils.common import errHander, doubleLog
import requests
from lxml import html
from conf import output_path
import time
import csv
import traceback
import random


def Downloader(url):
    r = requests.get(url, headers=getHeader1())
    r.encoding = 'utf8'
    if not r.text:
        doubleLog('response text empty!')
    return r.text


def Parser(text):
    res = []
    root = html.fromstring(text)
    lst = root.findall('.//ul[@class="listUl"]//li[@sortid]')
    succ_count = 0
    for item in lst:
        try:
            des = item.xpath('./div[@class="des"]')[0]
            title = des.xpath('./h2/a')[0].text
            room = des.xpath('./p[@class="room"]')[0].text
            room1, room2 = room.replace('\xa0', '').strip().split()
            add1 = des.xpath('./p[@class="add"]/a[1]')[0].text
            add2 = des.xpath('./p[@class="add"]/a[2]')[0].text

            listliright = item.xpath('./div[@class="listliright"]')[0]
            money = listliright.xpath('./div[@class="money"]/b')[0].text
            res.append([
                title.strip(),
                room1,  # 房型
                room2,  # 平米
                add1.strip(),
                add2.strip(),
                money.strip()
            ])
            succ_count += 1
        except Exception as e:
            traceback.print_exc()

    print('parse count: {}/{}'.format(succ_count, len(lst)))
    if not res:
        doubleLog('parser result empty')
    return res


def Outputer(lst, fname='', fpath=output_path):
    if not fname:
        fname = time.strftime('%Y%m%d%H%M') + '.csv'
    with open(fpath + fname, "a", newline="", encoding='utf-8-sig') as f:
        # f.write(codecs.BOM_UTF8)
        csv_writer = csv.writer(f, dialect='excel')
        csv_writer.writerows(lst)


def main():
    for i in range(1, 71):
        time.sleep(random.random() * 3)
        rent_personal = 'http://cs.58.com/chuzu/0/pn{}/'.format(i)
        print('#{} crawl: {}'.format(i, rent_personal))
        houseList = Parser(Downloader(rent_personal))
        if houseList:
            Outputer(houseList, fname='changsha_personal_rent.csv', fpath='./')
            print('#{} done'.format(i))

        time.sleep(random.random() * 3)
        rent_broker = 'http://cs.58.com/chuzu/1/pn{}/?PGTID=0d3090a7-0019-e2ea-e997-d2eac6339f64&ClickID=2'.format(i)
        houseList = Parser(Downloader(rent_broker))
        if houseList:
            Outputer(houseList, fname='changsha_broker_rent.csv', fpath='./')


if __name__ == '__main__':
    main()
