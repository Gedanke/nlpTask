import os
import json
import numpy
import pandas
import xgboost as xgb
from snownlp import SnowNLP
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics, svm, utils
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


INDEX = [
    "cs", "finance", "fun", "music", "skill", "study", "workplace"
]
ORPATH = "..\\..\\data\\barrage\\"
PATH = "..\\..\\result\\emotion\\"

stopwords = list()
with open("..\\..\\resource\\stopwords.txt", "r", encoding="utf8") as f:
    for w in f:
        stopwords.append(w.strip())

'''异常值纪录'''
error_bv = set()


class Bayes:
    """
    """

    def __init__(self, train, test):
        """

        Args:
            train (_type_): _description_
            test (_type_): _description_
        """
        self.train = train
        self.test = test

    def run(self):
        """
        """
        vectorizer = CountVectorizer(
            token_pattern='\[?\w+\]?',
            stop_words=stopwords
        )
        X_train = vectorizer.fit_transform(self.train["弹幕"])
        y_train = self.train["标签"]
        X_test = vectorizer.transform(self.test["弹幕"])
        y_test = self.test["标签"]
        clf = MultinomialNB()
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        pd = metrics.classification_report(y_test, y_pred)
        acc = metrics.accuracy_score(y_test, y_pred)
        auc = -1
        try:
            auc = metrics.roc_auc_score(y_test, y_pred)
        except ValueError:
            pass
        return pd, acc, auc


class Svm:
    """
    """

    def __init__(self, train, test):
        """

        Args:
            train (_type_): _description_
            test (_type_): _description_
        """
        self.train = train
        self.test = test

    def run(self):
        """
        """
        vectorizer = TfidfVectorizer(
            token_pattern='\[?\w+\]?',
            stop_words=stopwords
        )
        X_train = vectorizer.fit_transform(self.train["弹幕"])
        y_train = self.train["标签"]
        X_test = vectorizer.transform(self.test["弹幕"])
        y_test = self.test["标签"]
        clf = svm.SVC()
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        pd = metrics.classification_report(y_test, y_pred)
        acc = metrics.accuracy_score(y_test, y_pred)
        auc = -1
        try:
            auc = metrics.roc_auc_score(y_test, y_pred)
        except ValueError:
            pass
        return pd, acc, auc


class Xgboost:
    """
    """

    def __init__(self, train, test):
        """

        Args:
            train (_type_): _description_
            test (_type_): _description_
        """
        self.train = train
        self.test = test
        self.param = {
            'booster': 'gbtree',
            'max_depth': 6,
            'scale_pos_weight': 0.5,
            'colsample_bytree': 0.8,
            'objective': 'binary:logistic',
            'eval_metric': 'error',
            'eta': 0.3,
            'nthread': 10,
        }

    def run(self):
        """
        """
        vectorizer = CountVectorizer(
            token_pattern='\[?\w+\]?',
            stop_words=stopwords,
            max_features=2000
        )
        X_train = vectorizer.fit_transform(self.train["弹幕"])
        y_train = self.train["标签"]
        X_test = vectorizer.transform(self.test["弹幕"])
        y_test = self.test["标签"]
        dmatrix = xgb.DMatrix(X_train, label=y_train)
        model = xgb.train(
            self.param, dmatrix, num_boost_round=200
        )
        dmatrix = xgb.DMatrix(X_test)
        y_pred = model.predict(dmatrix)
        '''二值化'''
        y_pred = list(map(lambda x: 1 if x > 0.5 else 0, y_pred))
        pd = metrics.classification_report(y_test, y_pred)
        acc = metrics.accuracy_score(y_test, y_pred)
        auc = -1
        try:
            auc = metrics.roc_auc_score(y_test, y_pred)
        except ValueError:
            pass
        return pd, acc, auc


def k_fold(data, path, file):
    """

    Args:
        data (_type_): _description_
        path (_type_): _description_
        file (_type_): _description_
    """
    '''存放k折acc，auc'''
    result_bayes = dict()
    result_svm = dict()
    result_xgboost = dict()

    '''存放k折pandas.DataFrame'''
    writer_bayes = open(path + "bayes\\" + file + ".txt", "w")
    writer_svm = open(path + "svm\\" + file + ".txt", "w")
    writer_xgboost = open(path + "xgboost\\" + file + ".txt", "w")

    '''划分'''
    tmp_data = utils.shuffle(data)
    k = 10
    k_sample_count = tmp_data.shape[0] // k

    '''根据k折，划分数据集'''
    for fold in range(k):
        print(fold)
        validation_begin = k_sample_count * fold
        validation_end = k_sample_count * (fold + 1)
        '''验证集（或者叫测试集）'''
        validation_data = tmp_data[validation_begin:validation_end]

        '''训练集，pd.concat 沿着垂直的方向堆叠数据，拼接得到训练集'''
        train_data = pandas.concat([
            tmp_data[:validation_begin],
            tmp_data[validation_end:]
        ])
        '''重新索引（这一步可有可不有，看你自己情况，需要索引重新降序排列你就加）'''
        train_data.index = numpy.arange(len(train_data))
        validation_data.index = numpy.arange(len(validation_data))

        '''不同方法'''
        '''Bayes'''
        b = Bayes(train_data, validation_data)
        pd, ac, auc = b.run()
        if auc == -1:
            error_bv.add(path + "bayes\\" + file + ".txt")
            error_bv.add(path + "bayes\\" + file + ".json")
        else:
            result_bayes[fold + 1] = [
                ac, auc
            ]
            writer_bayes.write(pd + "\n")

        '''svm'''
        s = Svm(train_data, validation_data)
        pd, ac, auc = s.run()
        if auc == -1:
            error_bv.add(path + "svm\\" + file + ".txt")
            error_bv.add(path + "svm\\" + file + ".json")
        else:
            result_svm[fold + 1] = [
                ac, auc
            ]
            writer_svm.write(pd + "\n")

        '''xgboost'''
        x = Xgboost(train_data, validation_data)
        pd, ac, auc = x.run()
        if auc == -1:
            error_bv.add(path + "xgboost\\" + file + ".txt")
            error_bv.add(path + "xgboost\\" + file + ".json")
        else:
            result_xgboost[fold + 1] = [
                ac, auc
            ]
            writer_xgboost.write(pd + "\n")

    '''txt'''
    writer_bayes.close()
    writer_svm.close()
    writer_xgboost.close()

    '''json'''
    with open(path + "bayes\\" + file + ".json", "w", encoding="utf-8") as f:
        f.write(json.dumps(result_bayes, ensure_ascii=False))
    with open(path + "svm\\" + file + ".json", "w", encoding="utf-8") as f:
        f.write(json.dumps(result_svm, ensure_ascii=False))
    with open(path + "xgboost\\" + file + ".json", "w", encoding="utf-8") as f:
        f.write(json.dumps(result_xgboost, ensure_ascii=False))


def main():
    """
    主方法
    """
    for dir in INDEX:
        files = os.listdir(ORPATH + dir)
        for file in files:
            p = ORPATH + dir+"\\" + file
            print(p)
            data = pandas.read_csv(p)
            data["标签"] = 0
            l = len(data)
            '''赋予标签'''
            for i in range(l):
                s = SnowNLP(str(data.loc[i]["弹幕"])).sentiments
                data.loc[i, "标签"] = 0 if float(s) < 0.5 else 1
            save_path = PATH + dir + "\\"
            '''k 折交叉验证'''
            k_fold(data, save_path, file.split(".")[0])

    '''删除异常文件'''
    for f in error_bv:
        os.remove(f)


def test():
    """
    test
    """
    p = "..\\..\\data\\barrage\\cs\\BV1pE411c7tx.csv"
    data = pandas.read_csv(p)
    data["标签"] = 0
    l = len(data)
    for i in range(l):
        s = SnowNLP(str(data.loc[i]["弹幕"])).sentiments
        data.loc[i, "标签"] = 0 if float(s) < 0.5 else 1
    save_path = "..\\..\\result\\emotion\\cs\\"
    k_fold(data, save_path, "BV1pE411c7tx")
    for f in error_bv:
        os.remove(f)


if __name__ == '__main__':
    """
    """
    main()
    # test()
