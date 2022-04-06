import os
import numpy
import pandas
import pyecharts.options as opts
from pyecharts.charts import Bar


ORPARH = ""
SAVEPATH = ""


def draw_line(xlist, ylist):
    """

    Args:
        xlist (_type_): _description_
        ylist (_type_): _description_
    """
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='900px',
            js_host="./",
        ))
        .add_xaxis(xlist)
        .add_yaxis("互动指数", ylist)
        .set_global_opts(
            title_opts=opts.TitleOpts("TOP10互动指数视频"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
        .render(SAVEPATH + 'TOP10互动指数视频.html')
    )


def main():
    """
    """
    namelist = list()
    numlist = list()
    files = os.listdir(ORPARH)
    for file in files:
        data = pandas.read_csv(ORPARH + file, encoding='gb18030')
        for i in range(0, len(data)):
            namelist.append(data['名称'].iloc[i])
            if '万' in str(data['弹幕数'].iloc[i]):
                a = int(float(str(data['弹幕数'].iloc[i]).split('万')[0]) * 10000)
            else:
                a = int(data['弹幕数'].iloc[i])

            if '万' in str(data['播放量'].iloc[i]):
                b = int(float(str(data['播放量'].iloc[i]).split('万')[0]) * 10000)
            else:
                b = int(data['播放量'].iloc[i])

            c = round(a / b * 100, 2)
            numlist.append(c)

    nnum = numpy.array(numlist)
    snum = numpy.argsort(nnum)

    xlist = list()
    ylist = list()
    for i in range(1, 11):
        xlist.append(namelist[snum[0 - i]])
        ylist.append(numlist[snum[0 - i]])
    draw_line(xlist, ylist)


if __name__ == '__main__':
    """"""
    main()
