import os
import json
import numpy
import pandas
import matplotlib.pyplot as plt


INDEX = [
    "cs", "finance", "fun", "music", "skill", "study", "workplace"
]
ORPATH = "..\\..\\result\\emotion\\"

result = dict(
    zip(
        INDEX, [
            dict(
                zip(
                    ["bayes", "svm", "xgboost"], [
                        dict(
                            zip(
                                ["acc", "auc"], [[], []]
                            )
                        ) for _ in range(3)
                    ]
                )
            ) for _ in range(len(INDEX))
        ]
    )
)

"""
{'cs': {'bayes': {'acc': [], 'auc': []}, 
'svm': {'acc': [], 'auc': []}, 
'xgboost': {'acc': [], 'auc': []}}, 

'finance': {'bayes': {'acc': [], 'auc': []}, 'svm': {'acc': [], 'auc': []}, 'xgboost': {'acc': [], 'auc': []}}, 'fun': {'bayes': {'acc': [], 'auc': []}, 'svm': {'acc': [], 'auc': []}, 'xgboost': {'acc': [], 'auc': []}}, 'music': {'bayes': {'acc': [], 'auc': []}, 'svm': {'acc': [], 'auc': []}, 'xgboost': {'acc': [], 'auc': []}}, 'skill': {'bayes': {'acc': [], 'auc': []}, 'svm': {'acc': [], 'auc': []}, 'xgboost': {'acc': [], 'auc': []}}, 'study': {'bayes': {'acc': [], 'auc': []}, 'svm': {'acc': [], 'auc': []}, 'xgboost': {'acc': [], 'auc': []}}, 'workplace': {'bayes': {'acc': [], 'auc': []}, 'svm': {'acc': [], 'auc': []}, 'xgboost': {'acc': [], 'auc': []}}}
"""


def fq(dir):
    """
    不同分区
    Args:
        dir (_type_): _description_
    """
    path = ORPATH + dir + "\\"
    files = os.listdir(path + "bayes\\")
    for file in files:
        if file.split(".")[1] == "json":
            print(file)
            for method in ["bayes", "svm", "xgboost"]:
                print("method: ", method)
                data = dict()
                with open(path + method + "\\" + file, "r") as f:
                    data = json.load(f)
                acc = 0.0
                auc = 0.0
                for v in data.values():
                    acc += v[0]
                    auc += v[1]
                acc /= 10.0
                auc /= 10.0
                '''save'''
                result[dir][method]["acc"].append(acc)
                result[dir][method]["auc"].append(auc)


def mine_plot(channel, method):
    """
    专区可视化
    三张图，三种方法,多子图
    纵坐标为acc，auc 的值 0-1
    横坐标为折数，1-10
    Args:
        metho (_type_): _description_
        channel (_type_): _description_
    """
    path = ORPATH + channel + "\\" + method + "\\"
    '''ax1 是acc，ax2 是auc'''
    plt.figure(figsize=(20, 8))
    plt.title(method)
    '''file'''
    files = os.listdir(path)
    x = [i for i in range(1, 11)]

    lenged_list = list()
    for file in files:
        if file.split(".")[1] == "json":
            print(file.split(".")[0])
            lenged_list.append(file.split(".")[0])
            p = path + file
            data = dict()
            with open(p, "r") as f:
                data = json.load(f)
            acc_y = list()
            auc_y = list()
            for v in data.values():
                acc_y.append(v[0])
                auc_y.append(v[1])
            ''''''
            plt.subplot(1, 2, 1)
            plt.plot(x, acc_y)

            ''''''
            plt.subplot(1, 2, 2)
            plt.plot(x, auc_y)

    params = {
        'legend.fontsize': 7,
        'legend.handlelength': 4
    }
    ''''''
    plt.subplot(1, 2, 1)
    plt.xticks(x)
    plt.title("acc")
    plt.rcParams.update(params)
    plt.legend(lenged_list)

    plt.subplot(1, 2, 2)
    plt.xticks(x)
    plt.title("auc")
    plt.rcParams.update(params)
    plt.legend(lenged_list)

    plt.savefig(ORPATH + "show\\" + channel + "_" + method + ".png")
    # plt.show()


def save_result():
    """
    
    """
    for dir in INDEX:
        print(ORPATH + dir + "\\")
        fq(dir)
    '''save'''
    with open(ORPATH + "table.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False))


def save_figure():
    """
    """
    for dir in INDEX:
        for method in ["bayes", "svm", "xgboost"]:
            mine_plot(dir, method)


def print_table():
    """
    """
    r = dict()
    with open(ORPATH + "table.json", "r", encoding="utf-8") as f:
        r = json.load(f)
    for cha in INDEX:
        print("分区: ", cha)
        for me in ["bayes", "svm", "xgboost"]:
            print("方法: ", me)
            acc_l = r[cha][me]["acc"]
            acc_mean = numpy.mean(acc_l)
            acc_std = numpy.std(acc_l)
            print("acc mean: ", acc_mean, "acc std: ", acc_std)
            auc_l = r[cha][me]["auc"]
            acc_mean = numpy.mean(auc_l)
            acc_std = numpy.std(auc_l)
            print("acc mean: ", acc_mean, "acc std: ", acc_std)


if __name__ == '__main__':
    """
    """
    # save_result()
    # print(result)
    # save_figure()
    print_table()
