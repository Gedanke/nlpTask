import os
import numpy
import pandas
import pyecharts.options as opts
from pyecharts.charts import Bar

ORPARH = ""
SAVEPATH = ""


def draw_line(xlist, ylist, ylist2):
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='900px',
            js_host="./",
        ))
        .add_xaxis(xlist)
        .add_yaxis("视频平均弹幕数", ylist)
        .add_yaxis("视频最高弹幕数", ylist2)
        .set_global_opts(
            title_opts=opts.TitleOpts("平均-最高弹幕数"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
        .render(SAVEPATH+'平均-最高弹幕数.html')
    )


def main():
    """
    """
    xlist = list()
    ylist = list()
    ylist2 = list()

    files = os.listdir(ORPARH)
    for file in files:
        numlist = []
        data = pd.read_csv(ORPARH + file, encoding='gb18030')
        xlist.append(file.split('.')[0])
        for i in range(0, len(data)):
            if '万' in str(data['弹幕数'].iloc[i]):
                numlist.append(
                    int(float(str(data['弹幕数'].iloc[i]).split('万')[0]) * 10000))
            else:
                numlist.append(int(data['弹幕数'].iloc[i]))
        ylist.append(round(sum(numlist) / len(data), 2))
        ylist2.append(max(numlist))

    draw_line(xlist, ylist, ylist2)


if __name__ == '__main__':
    """"""
    main()
