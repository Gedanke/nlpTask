import os
import numpy
import pandas
import pyecharts.options as opts
from pyecharts.charts import Bar


ORPARH = ""
SAVEPATH = ""


def draw_line(xlist, ylist, ylist2):
    """

    Args:
        xlist (_type_): _description_
        ylist (_type_): _description_
        ylist2 (_type_): _description_
    """
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='900px',
            js_host="./",
        ))
        .add_xaxis(xlist)
        .add_yaxis("视频平均互动指数", ylist)
        .add_yaxis("视频最高互动指数", ylist2)
        .set_global_opts(
            title_opts=opts.TitleOpts("平均-最高互动指数"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
        .render(SAVEPATH + '平均-最高互动指数.html')
    )


def main():
    """"""
    xlist = list()
    ylist = list()
    ylist2 = list()

    files = os.listdir(ORPARH)
    for file in files:
        numlist = list()
        data = pd.read_csv(ORPARH + file, encoding='gb18030')
        xlist.append(file.split('.')[0])
        for i in range(0, len(data)):
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
        ylist.append(round(sum(numlist) / len(data), 2))
        ylist2.append(max(numlist))

    draw_line(xlist, ylist, ylist2)


if __name__ == '__main__':
    """"""
    main()
