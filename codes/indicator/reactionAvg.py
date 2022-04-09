import os
import numpy
import pandas
import pyecharts.options as opts
from pyecharts.charts import Bar


ORPATH = "..\\..\\resource\\origin\\"
SAVEPATH = "..\\..\\result\\indicator\\"
UPPATH = "..\\..\\data\\upMsg\\up主粉丝数.csv"
index_dict = {
    "cs": "IT区", "finance": "金融区", "fun": "搞笑区",
    "music": "音乐区", "skill": "技巧区", "study": "学习区", "workplace": "职场区"
}


def draw_line(xlist, ylist, ylist2):
    """_summary_

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
        .add_yaxis("视频平均粉丝响应指数", ylist)
        .add_yaxis("视频最高粉丝响应指数", ylist2)
        .set_global_opts(
            title_opts=opts.TitleOpts("平均-最高粉丝响应指数"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
        .render(SAVEPATH + '平均-最高粉丝响应指数.html')
    )


def main():
    """
    """
    fansfile = pandas.read_csv(UPPATH)
    dict_country = fansfile.set_index('uid').T.to_dict('list')

    xlist = list()
    ylist = list()
    ylist2 = list()

    files = os.listdir(ORPATH)
    for file in files:
        numlist = list()
        data = pandas.read_csv(ORPATH + file)
        xlist.append(file.split('.')[0])
        for i in range(0, len(data)):
            a = dict_country[data['up主id'].iloc[i]][1]

            if '万' in str(data['播放量'].iloc[i]):
                b = int(float(str(data['播放量'].iloc[i]).split('万')[0]) * 10000)
            else:
                b = int(data['播放量'].iloc[i])

            c = round(b / a, 2)
            numlist.append(c)
        ylist.append(round(sum(numlist) / len(data), 2))
        ylist2.append(max(numlist))

    xlist = [
        v for v in index_dict.values()
    ]
    draw_line(xlist, ylist, ylist2)


if __name__ == '__main__':
    """"""
    main()
