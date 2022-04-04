import json
import pandas
import time
import requests
import os
import re


info_table = pandas.DataFrame(columns=['uid', 'follower'])
row_cnt = 1
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}
# 不设置代理
proxies = {
    "http": None,
    "https": None
}
PATH = "..\\..\\data\\upmsg\\"
ORPATH = "..\\..\\resource\\origin\\"


def get_fs(url):
    global info_table, row_cnt

    res = requests.get(url, headers=headers, proxies=proxies)
    rep = json.loads(res.text)
    alist = []
    alist.append(rep['data']['mid'])
    alist.append(rep['data']['follower'])
    info_table.loc[row_cnt] = alist
    row_cnt += 1
    info_table.to_csv(PATH+'up主粉丝数.csv', encoding='gb18030')


def main():
    """
    """
    uplist = list()
    filenames = os.listdir(ORPATH)  # 设定调用文件的相对路径
    f = list()
    for i in filenames:
        if '.csv' in str(i):
            f.append(i)
    for i in f:
        data = pd.read_csv(ORPATH + i, encoding='gb18030')
        for j in data['up主id']:
            if j in uplist:
                continue
            else:
                uplist.append(j)
                url = 'https://api.bilibili.com/x/relation/stat?vmid=' + \
                    str(j) + '&jsonp=jsonp'
                get_fs(url)
                print('finished', j)


if __name__ == '__main__':
    """"""
