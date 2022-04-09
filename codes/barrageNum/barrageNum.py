import os
import numpy
import pandas
import pyecharts.options as opts
from pyecharts.charts import Bar

ORPATH = "..\\..\\resource\\origin\\"
SAVEPATH = "..\\..\\result\\barrage\\"


def draw_line(xlist, ylist):
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='900px',
            js_host="./",
        ))
        .add_xaxis(xlist)
        .add_yaxis("视频弹幕数", ylist)
        .set_global_opts(
            title_opts=opts.TitleOpts("TOP弹幕视频"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
        .render(SAVEPATH + 'TOP弹幕视频.html')
    )


def main():
    """
    """
    namelist = list()
    numlist = list()
    files = os.listdir(ORPATH)
    for file in files:
        data = pandas.read_csv(ORPATH + file,encoding="utf-8")
        for i in range(0, len(data)):
            namelist.append(data['名称'].iloc[i])
            if '万' in str(data['弹幕数'].iloc[i]):
                numlist.append(
                    int(float(str(data['弹幕数'].iloc[i]).split('万')[0]) * 10000)
                )
            else:
                numlist.append(int(data['弹幕数'].iloc[i]))

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
    
