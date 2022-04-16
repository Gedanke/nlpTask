import os
import re
import json
import time
import pandas
import random
import requests


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
PATH = "..\\..\\data\\upMsg\\"
ORPATH = "..\\..\\resource\\origin\\"
INDEX = [
    "cs", "finance", "fun", "music", "skill", "study", "workplace"
]


def get_fs(url):
    """

    Args:
        url (_type_): _description_
    """
    global info_table, row_cnt

    res = requests.get(
        url, headers=headers, proxies=proxies
    )
    rep = json.loads(res.text)
    alist = list()
    alist.append(rep['data']['mid'])
    alist.append(rep['data']['follower'])
    info_table.loc[row_cnt] = alist
    row_cnt += 1
    info_table.to_csv(PATH + 'up主粉丝数.csv')


def main():
    """
    """
    f = list()
    uplist = list()
    filenames = os.listdir(ORPATH)  # 设定调用文件的相对路径
    for i in filenames:
        if '.csv' in str(i):
            f.append(i)

    for i in f:
        data = pandas.read_csv(ORPATH + i)
        for j in data['up主id']:
            if j in uplist:
                continue
            else:
                uplist.append(j)
                url = 'https://api.bilibili.com/x/relation/stat?vmid=' + \
                    str(j) + '&jsonp=jsonp'
                time.sleep(random.randint(2, 5))
                get_fs(url)
                print('finished', j)


if __name__ == '__main__':
    """"""
    main()
