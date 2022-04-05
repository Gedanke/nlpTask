# readme

bilibili 视频弹幕分析，含爬虫，数据处理，词云分析，词频分析，情感分析，可视化等等

所需库:

```shell

```

项目目录如下：

* [codes](codes): 程序代码
    * [dataScrape](codes/dataScrape/): 通过bv号爬取数据
    * [wordCloud](codes/wordCloud/): 得到词云
    * [barrageNum](codes/barrageNum/): 弹幕数量
    * [indicator](codes/indicator/): 构建指标
    * [emotionAnalysis](codes/emotionAnalysis/): 情感分析
* [data](data): 爬虫获取并清洗后的数据
    * [barrage](data/barrage/): 弹幕数据，仅含有弹幕文本，数量有限
    * [barrages](data/barrages/): 弹幕数据，含有全部的弹幕，同时含有每条弹幕的详细信息，例如发送者，弹幕格式等等
    * [barragesData](data/barragesData/): 从全部弹幕提取出的弹幕文本
* [resource](resource): 存放资源
    * [vedio.txt](resource/vedio.txt): 存放视频bv号的文本文件
* [result](result): 存放结果
* [readme](readme.md): 说明文件

