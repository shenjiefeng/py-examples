# encoding: utf-8
__author__ = 'fengshenjie'
from fsjutils import GetHeaderV1, Downloader
from lxml import html
import traceback
import pandas as pd
from datetime import datetime
import re
from view import word_cloud_plot, area_price_plot, area_plot

report_file = './report.csv'
RE_INT = re.compile(r'[-+]?([\d\.]+)')


class HouseInfo:
    agg_page = ''
    title = ''
    room_type = ''
    area = ''
    floor = ''
    direction = ''
    year = ''
    person = ''  # owner or broker

    name = ''
    address = ''

    price = ''
    price_per_square = ''

    err = ''

    def __str__(self):
        return ' '.join((
            self.title, self.room_type, self.area, self.floor, self.direction, self.year, self.person, '; ',
            self.name, self.address, self.price, self.price_per_square))

    def __repr__(self):
        return self.__str__()

    def toDict(self):
        return {
            'page': self.agg_page,
            'title': self.title,
            'room_type': self.room_type,
            'area': self.area,
            'floor': self.floor,
            'direction': self.direction,
            'year': self.year,
            'person': self.person,
            'xiaoqu_name': self.name,
            'address': self.address,
            'price': self.price,
            'price_per_square': self.price_per_square,
        }


def _getSource(url):
    header = GetHeaderV1()
    text = Downloader(url, header, encoding='gb2312')
    return text


def _parser(page, url):
    text = _getSource(url)
    print(datetime.now(), 'crawl', url)
    root = html.fromstring(text)
    lst = root.findall('.//div[@class="shop_list shop_list_4"]/dl')

    houseLst = []
    print('loop', len(text), len(lst))
    for node in lst:
        thehouse = HouseInfo()
        thehouse.agg_page = page
        try:
            thehouse.title = node.find('.//dd/h4/a').xpath('@title')[0]
            ''' Get all text inside a tag in lxml
            ([c.text, tostring(c), c.tail] for c in node.getchildren())
            '''
            detail_line1 = node.find('.//dd/p[@class="tel_shop"]').xpath('text()')
            thehouse.room_type = detail_line1[0].strip()
            thehouse.area = detail_line1[1].strip()
            if thehouse.area:
                thehouse.area = RE_INT.findall(thehouse.area)[0]
            thehouse.floor = detail_line1[2].strip()
            thehouse.direction = detail_line1[3].strip()
            thehouse.year = detail_line1[4].strip()
            thehouse.person = node.find('.//dd/p[@class="tel_shop"]/span/a').xpath('text()')[0].strip()

            detail_line2 = node.find('.//dd/p[@class="add_shop"]').xpath('.//text()')  # 当前节点下的所有text
            thehouse.name = detail_line2[1].strip()
            thehouse.address = detail_line2[3].strip()

            detail_line3 = node.find('.//dd[@class="price_right"]').xpath('.//text()')
            thehouse.price = detail_line3[1].strip()
            thehouse.price_per_square = detail_line3[4].strip()
            if thehouse.price_per_square:
                thehouse.price_per_square = RE_INT.findall(thehouse.price_per_square)[0]
        except Exception as e:
            thehouse.err = str(e)
            traceback.print_exc()
        houseLst.append(thehouse)
    print(datetime.now(), 'done', len(houseLst))
    return houseLst


def view(df):
    assert isinstance(df, pd.DataFrame)
    df = df.dropna()
    word_cloud_plot(df)
    area_plot(df)
    area_price_plot(df)

    return


def main():
    # i31 to i3100
    url = 'http://sh.esf.fang.com/house/i3{}/'
    houseLst = []
    for i in range(1, 101):
        houseLst.extend(_parser(i, url.format(i)))

    finalDf = pd.DataFrame([i.toDict() for i in houseLst])
    view(finalDf)
    finalDf.to_csv(report_file, index=False, encoding='utf_8_sig')
    return houseLst


if __name__ == '__main__':
    main()
