import os
import jieba
import numpy
import pandas
import matplotlib.pyplot as plt
from snownlp import SnowNLP


INDEX = [
    "cs", "finance", "fun", "music", "skill", "study", "workplace"
]
ORPATH = "..\\..\\data\\barrage\\"
PATH = "..\\..\\result\\emotion\\"
index_dict = {
    "cs": "IT区", "finance": "金融区", "fun": "搞笑区",
    "music": "音乐区", "skill": "技巧区", "study": "学习区", "workplace": "职场区"
}


def build_sentimental_analysis(file_name, dir):
    """

    Args:
        file_name (_type_): _description_
        dir (_type_): _description_

    Returns:
        _type_: _description_
    """
    comment_list = list()
    for i in file_name:
        file = pandas.read_csv(ORPATH + i[0] + '\\' + i[1])
        for j in file['弹幕']:
            comment_list.append(j)

    # 切词
    # word_list = word_cut(comment_list)

    #建立情感分析
    sentimental_list = list()
    for i in comment_list:
        s = SnowNLP(i)
        sentimental_list.append(s.sentiments)

    avg = round(sum(sentimental_list) / len(sentimental_list), 4)
    plt.hist(
        sentimental_list, bins=numpy.arange(0, 1, 0.01), facecolor='g'
    )
    plt.xlabel('Sentiments Probability')
    plt.ylabel('Quantity')
    plt.title('Analysis of Sentiments')
    # plt.show()
    plt.savefig(PATH + index_dict[dir] + '视频弹幕情感分析.png')
    return avg


def read_file():
    """
    """
    info_table = pandas.DataFrame(columns=['频道', '平均情感指数'])
    row_cnt = 1
    for dir in INDEX:
        file_list = list()
        files = os.listdir(ORPATH + dir)
        for file in files:
            tmp = list()
            tmp.append(dir)
            tmp.append(file)
            file_list.append(tmp)
        avg = build_sentimental_analysis(file_list, dir)
        print(avg)
        alist = list()
        alist.append(dir)
        alist.append(avg)
        info_table.loc[row_cnt] = alist
        row_cnt += 1
    info_table.to_csv(PATH + '各频道情感系数.csv')


if __name__ == '__main__':
    """
    """
    read_file()
