import os
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
        # print(metrics.classification_report(y_test, y_pred))
        # print("准确率:", metrics.accuracy_score(y_test, y_pred))
        return metrics.classification_report(y_test, y_pred), metrics.accuracy_score(y_test, y_pred)


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
        return metrics.classification_report(y_test, y_pred), metrics.accuracy_score(y_test, y_pred)


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
        '''先计算AUC'''
        auc_score = metrics.roc_auc_score(y_test, y_pred)          
        '''二值化'''
        y_pred = list(map(lambda x:1 if x > 0.5 else 0, y_pred))   
        print(metrics.classification_report(y_test, y_pred))
        print("准确率:", metrics.accuracy_score(y_test, y_pred))
        print("AUC:", auc_score)
        
def k_fold(data):
    """

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    result_acc_bayes = dict()

    tmp_data = utils.shuffle(data)
    k = 10
    k_sample_count = tmp_data.shape[0] // k

    '''根据k折，划分数据集'''
    for fold in range(k):
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

        '''不同方法 '''
        # b=Bayes(train_data, validation_data)
        # pd,ac=b.run()
        # result_acc_bayes[fold+1]=ac
        # s = Svm(train_data, validation_data)
        # pd, ac = s.run()
        # print(pd)
        # print(ac)
        x=Xgboost(train_data, validation_data)
        x.run()

def main():
    """
    """
    for dir in INDEX:
        files = os.listdir(ORPATH+dir)
        for file in files:
            p = ORPATH+dir+"\\" + file
            data = pandas.read_csv(p)
            data["标签"] = 0
            l = len(d)
            for i in range(l):
                s = SnowNLP(str(data.loc[i]["弹幕"])).sentiments
                data.loc[i, "标签"] = 0 if float(s) < 0.5 else 1
                k_fold(data)


def test():
    """"""
    p = "..\\..\\data\\barrage\\cs\\BV1aE411o7qd.csv"
    data = pandas.read_csv(p)
    data["标签"] = 0
    l = len(data)
    for i in range(l):
        s = SnowNLP(str(data.loc[i]["弹幕"])).sentiments
        data.loc[i, "标签"] = 0 if float(s) < 0.5 else 1
    k_fold(data)


if __name__ == '__main__':
    """
    """
    # main()
    test()
