# encoding: utf-8
__author__ = 'fengshenjie'
from pyecharts import Line, Bar, Overlap, Pie
import pandas as pd
import jieba
import wordcloud


def area_plot(df):
    # 房屋面积分布
    bins = [0, 30, 60, 90, 120, 150, 200, 300, 400, 700]
    level = ['0-30', '30-60', '60-90', '90-120', '120-150', '150-200', '200-300', '300-400', '400+']
    df['area'] = df['area'].astype(float)
    df['square_level'] = pd.cut(df['area'], bins=bins, labels=level)

    df_digit = df[
        ['address', 'area', 'direction', 'floor', 'page', 'person', 'price',
         'price_per_square', 'room_type', 'title', 'xiaoqu_name', 'year',
         'square_level']]
    s = df_digit['square_level'].value_counts()

    attr = s.index
    v1 = s.values

    pie = Pie("房屋面积分布", title_pos='center')

    pie.add(
        "",
        attr,
        v1,
        radius=[40, 75],
        label_text_color=None,
        is_label_show=True,
        legend_orient="vertical",
        legend_pos="left",
    )

    overlap = Overlap()
    overlap.add(pie)
    overlap.render('area_plot.html')


def area_price_plot(df):
    # 房屋面积&价位分布
    bins = [0, 30, 60, 90, 120, 150, 200, 300, 400, 700]
    level = ['0-30', '30-60', '60-90', '90-120', '120-150', '150-200', '200-300', '300-400', '400+']
    df['square_level'] = pd.cut(df['area'], bins=bins, labels=level)
    square = df[['square_level', 'price']]
    prices = square.groupby('square_level').mean().reset_index()
    amount = square.groupby('square_level').count().reset_index()

    attr = prices['square_level']
    v1 = prices['price']

    pie = Bar("房屋面积&价位分布布")
    pie.add("", attr, v1, is_label_show=True)
    pie.render()
    bar = Bar("房屋面积&价位分布")
    bar.add("", attr, v1, is_stack=True, xaxis_rotate=30, yaxix_min=4.2,
            xaxis_interval=0, is_splitline_show=False)

    overlap = Overlap()
    overlap.add(bar)
    overlap.render('area_price_plot.html')


def word_cloud_plot(df, pictureName='wcplot.jpg'):
    text = ' '.join(df['title'])
    cut_text = ' '.join(jieba.cut(text))

    '''
     OSError: cannot open resource, if font_path is None
    '''
    cloud = wordcloud.WordCloud(
        background_color='white',
        # font_path='yahei.ttf',
        font_path='STHeiti Light.ttc',  # mac 黑体
        max_words=1000,
        max_font_size=100,
    ).generate(cut_text)
    cloud.to_file(pictureName)
