import os
import pandas
import jieba
from wordcloud import WordCloud


PATH1 = "..\\..\\result\\wordCloud\\"
PATH2 = "..\\..\\result\\wordCount\\"
ORPATH = "..\\..\\data\\barrage\\"
INDEX = [
    "cs", "finance", "fun", "music", "skill", "study", "workplace"
]

index_dict = {
    "cs": "IT区", "finance": "金融区", "fun": "搞笑区",
    "music": "音乐区", "skill": "技巧区", "study": "学习区", "workplace": "职场区"
}


def drawWordCloud(words, title):
    """
    定义一个词云绘制函数，通过词频绘制词云图并写出到特定目录
    Args:
        words (_type_): _description_
        title (_type_): _description_
    """
    path = os.path.abspath('..')
    if not os.path.exists(PATH1):
        os.mkdir(PATH1)
    '''使用原先准备好的一张照片作为背景图'''
    wc = WordCloud(
        font_path='simkai.ttf', max_words=200, width=1920, height=1080, margin=5, background_color="white"
    )
    wc.generate_from_frequencies(words)
    wc.to_file(os.path.join(PATH1, title+'.png'))


def statistics(texts, stopwords):
    """
    使用jieba库来进行分词，并统计词语出现次数
    Args:
        texts (_type_): _description_
        stopwords (_type_): _description_

    Returns:
        _type_: _description_
    """
    words_dict = dict()
    for text in texts:
        temp = jieba.cut(text, cut_all=True)
        for t in temp:
            if t in stopwords:
                continue
            if t in words_dict.keys():
                words_dict[t] += 1
            else:
                words_dict[t] = 1
    return words_dict


def save(words_dict1, savename):
    """

    Args:
        words_dict1 (_type_): _description_
        savename (_type_): _description_
    """
    dict_list = list(words_dict1.keys())
    value_list = list(words_dict1.values())
    df = pandas.DataFrame(columns=['词语', '次数'])
    row = 0
    for i in range(0, len(dict_list)):
        alist = list()
        alist.append(dict_list[i])
        alist.append(value_list[i])
        df.loc[row] = alist
        row += 1
    df.to_csv(PATH2 + savename + '.csv')


if __name__ == '__main__':
    """"""
    stopwords = open(
        '..\\..\\resource\\stopwords.txt', 'r', encoding='utf-8'
    ).read()
    for d in INDEX:
        danmu = list()
        files = os.listdir(ORPATH + d + "\\")
        for file in files:
            data = pandas.read_csv(
                ORPATH + d + "\\" + file
            )
            for i in data["弹幕"]:
                danmu.append(i)
        words_dict = statistics(danmu, stopwords)
        save(
            words_dict, savename=index_dict[d] + '词频表'
        )
        drawWordCloud(
            words_dict, index_dict[d] + '词云图'
        )
