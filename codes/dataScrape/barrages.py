import re
import csv
import time
import json
import pandas
import random
import requests


# 不设置代理
proxies = {
    "http": None,
    "https": None
}
ORPATH = "..\\..\\resource\\origin\\"
# 保存路径
PATH = "..\\..\\data\\barrageData\\"
INDEX = [
    "cs", "finance", "fun", "music", "skill", "study", "workplace"
]


def get_content(page, cid):
    """
    获取弹幕
    Args:
        page (_type_): _description_
        cid (_type_): _description_

    Returns:
        _type_: _description_
    """
    url = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid={}&pid=40112794&segment_index={}'.format(
        cid, page)
    headers = {
        "authority": "api.bilibili.com",
        "method": "GET",
        "path": "/x/v2/dm/web/seg.so?type=1&oid={}&pid=40112794&segment_index={}".format(cid, page),
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "buvid3=3B61288D-B886-6198-5112-1F705E7EB43369808infoc; CURRENT_FNVAL=80; _uuid=BBC2D6F3-BB14-2900-4B78-43D4A194BEBF50856infoc; blackside_state=1; sid=7w15wel6; rpdid=|(JYlmuluumR0J'uYkRkR||l); Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1624240436; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1624240436; PVID=2; bfe_id=5db70a86bd1cbe8a88817507134f7bb5",
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/av40112794/",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",

    }
    r = requests.get(
        url=url, headers=headers, proxies=proxies
    ).text
    return r


def get_data(r, i, bv):
    """
    正则表达式匹配弹幕内容
    Args:
        r (_type_): _description_
        bv (_type_): _description_
    """
    data_list = re.findall(':(.*?)@', r)
    with open(PATH + i + "\\" + bv + ".csv", 'a', encoding="gb18030", newline='') as f:
        writer = csv.writer(f)
        if len(data_list) > 0:
            for data in data_list:
                writer.writerow([data])


def get_cid(bvid):
    """
    获取弹幕cid
    Args:
        bvid (_type_): _description_

    Returns:
        _type_: _description_
    """
    url = 'https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(
        bvid)
    headers = {
        "authority": "api.bilibili.com",
        "method": "GET",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://www.bilibili.com",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    }
    r = requests.get(
        url=url, headers=headers, proxies=proxies
    ).text
    cid_list = list()
    dictr = json.loads(r)
    data_list = dictr['data']
    for data in data_list:
        cid = data['cid']
        cid_list.append(cid)
    return cid_list


if __name__ == '__main__':
    """
    全弹幕收集，可以跑通，但是很花时间
    """
    for i in INDEX:
        path = ORPATH + i + ".csv"
        pd = pandas.read_csv(path)
        print(path)
        time.sleep(random.randint(12, 20))
        for bv in pd["BV号"]:
            print(bv, i)
            '''由bv号得到cid列表'''
            cid_list = get_cid(bv)
            for cid in cid_list:
                for page in range(1, 20):
                    r = get_content(page, cid)
                    get_data(r, i, bv)
                    time.sleep(random.randint(1, 3))
                time.sleep(random.randint(5, 10))
            print('finished', bv)
