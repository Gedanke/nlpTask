import re
import time
import pandas
import requests
from lxml import etree

# 请求头
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

# 视频url前缀
ROOT_URL = "https://m.bilibili.com/video/"
# 不设置代理
proxies = {
    "http": None,
    "https": None
}
# 保存路径
PATH="..\\..\\data\\barrage\\"

class BilibiliSpider:
    def __init__(self, BV):
        """
        构造要爬取的视频url地址
        Args:
            BV (_type_): _description_
        """
        self.BV = BV
        self.BVurl = ROOT_URL+BV
        self.info_table = pandas.DataFrame(columns=['弹幕'])
        self.row_cnt = 1

    def getXml_url(self):
        """
        获取该视频网页的内容
        Returns:
            _type_: _description_
        """
        '''弹幕都是在一个url请求中，该url请求在视频url的js脚本中构造'''
        response = requests.get(
            self.BVurl, headers=headers, proxies=proxies
        )
        html_str = response.content.decode()
        '''
        使用正则找出该弹幕地址
        格式为：https://comment.bilibili.com/168087953.xml
        我们分隔出的是地址中的弹幕文件名，即 168087953
        '''
        getWord_url = re.findall("cid:(.*?),", html_str)
        getWord_url = getWord_url[0].replace("+", "").replace(" ", "")
        '''组装成要请求的xml地址'''
        xml_url = "https://comment.bilibili.com/{}.xml".format(getWord_url)
        return xml_url

    def parse_url(self, url):
        """
        Xpath 不能解析指明编码格式的字符串，所以此处我们不解码，还是二进制文本
        Args:
            url (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = requests.get(
            url, headers=headers, proxies=proxies
        )
        return response.content

    #
    def get_word_list(self, str):
        """
        弹幕包含在xml中的<d></d>中，取出即可
        Args:
            str (_type_): _description_
        Returns:
            _type_: _description_
        """
        html = etree.HTML(str)
        word_list = html.xpath("//d/text()")
        return word_list

    def run(self):
        """
        """
        '''根据BV号获取弹幕的地址'''
        start_url = self.getXml_url()
        '''请求并解析数据'''
        xml_str = self.parse_url(start_url)
        word_list = self.get_word_list(xml_str)
        for word in word_list:
            alist = list()
            alist.append(word)
            self.info_table.loc[self.row_cnt] = alist
            self.row_cnt += 1
        self.info_table.to_csv(PATH+self.BV + '.csv', encoding='gb18030')


if __name__ == "__main__":
    """"""
    bv_list=list()
    bv_list=open("..\\..\\resource\\vedio.txt","r").readlines()
    for bv in bv_list:
        bv=bv.strip("\n")
        spider = BilibiliSpider(bv)
        spider.run()
        time.sleep(1)
        print('finished', bv)
