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
info_table = pandas.DataFrame(columns=['BV号', '情感指数'])
row_cnt = 1


def build_sentimental_analysis(file_name):
    """

    Args:
        file_name (_type_): _description_
    """
    global info_table, row_cnt

    for i in file_name:
        comment_list = list()
        file = pandas.read_csv(ORPATH + i[0] + '\\' + i[1])
        for j in file['弹幕']:
            comment_list.append(j)

        #建立情感分析
        sentimental_list = list()
        for j in comment_list:
            s = SnowNLP(j)
            sentimental_list.append(s.sentiments)
        avg = round(sum(sentimental_list) / len(sentimental_list), 4)
        alist = list()
        alist.append(i[1])
        alist.append(avg)
        info_table.loc[row_cnt] = alist
        row_cnt += 1
        print('finished', i[0])
    info_table.to_csv(PATH + '各视频弹幕情感分析.csv')


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
