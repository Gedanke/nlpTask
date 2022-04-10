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


def build_sentimental_analysis(file_name):
    """

    Args:
        file_name (_type_): _description_
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

    plt.hist(
        sentimental_list, bins=numpy.arange(0, 1, 0.01), facecolor='g'
    )
    plt.xlabel('Sentiments Probability')
    plt.ylabel('Quantity')
    plt.title('Analysis of Sentiments')
    # plt.show()
    plt.savefig(PATH + '全区视频弹幕情感分析.png')


def read_file():
    """
    """
    file_list = list()
    for dir in INDEX:
        files = os.listdir(ORPATH + dir)
        for file in files:
            tmp = list()
            tmp.append(dir)
            tmp.append(file)
            file_list.append(tmp)
    build_sentimental_analysis(file_list)


if __name__ == '__main__':
    """
    """
    read_file()
