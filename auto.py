# 爬取4今日热点事件排行榜
import requests
import json
import re
from bs4 import BeautifulSoup

require = 9


def get_data_baidu(url, headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    html = r.text
    data = []
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all(class_="item-wrap_2oCLZ")
    for i in range(len(content)):
        topic_name = content[i].find(class_="name_2Px2N").get_text().strip()
        topic_url = content[i]['href'].strip()
        print(topic_name, topic_url)
        tmp = "<a href='{}' class='list-group-item list-group-item-action' target='blank'> <span class='float-left text-primary'>{}</span><span class='title'>{}</span> </a>".format(
            topic_url, i+1, topic_name)
        data.append(tmp)
        if (i >= require):
            break
    return data


def get_data_zhihu(url, headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    html = r.text

    data = []
    soup = BeautifulSoup(html, "html.parser")
    hot_data = soup.find('script', id='js-initialData').string
    hot_json = json.loads(hot_data)
    hot_list = hot_json['initialState']['topstory']['hotList']
    # print(type(hot_list))
    for i in range(len(hot_list)):
        topic_name = hot_list[i]['target']['titleArea']['text']
        topic_url = hot_list[i]['target']['link']['url']
        print(topic_name, topic_url)
        tmp = "<a href='{}' class='list-group-item list-group-item-action' target='blank'> <span class='float-left text-primary'>{}</span><span class='title'>{}</span> </a>".format(
            topic_url, i+1, topic_name)
        data.append(tmp)
        if (i >= require):
            break
    return data


def get_data_weibo(url, headers):
    data = []
    r = requests.get(url, headers=headers)  
    data_json = r.json()['data']['realtime']
    # print(data_json)
    for data_item in data_json:
        topic_name = data_item['note']
        topic_url = 'https://s.weibo.com/weibo?q=%23' + data_item['word'] + '%23'
        i = data_item['rank']
        print(topic_name, topic_url)
        tmp = "<a href='{}' class='list-group-item list-group-item-action' target='blank'> <span class='float-left text-primary'>{}</span><span class='title'>{}</span> </a>".format(
            topic_url, i+1, topic_name)
        data.append(tmp)
        if (i >= require):
            break
    return data

def get_data_bilibili(url, headers):
    data = []
    i = 0
    r = requests.get(url, headers=headers)  
    data_json = r.json()['data']['list']
    # print(data_json)
    for data_item in data_json:
        topic_name = data_item['title']
        topic_url = 'https://www.bilibili.com/video/' + data_item['bvid']
        print(topic_name, topic_url)
        tmp = "<a href='{}' class='list-group-item list-group-item-action' target='blank'> <span class='float-left text-primary'>{}</span><span class='title'>{}</span> </a>".format(
            topic_url, i+1, topic_name)
        data.append(tmp)
        i = i+1
        if (i >= require):
            break
    return data

def main():
    url_baidu = 'https://top.baidu.com/board?tab=homepage'
    url_zhihu = 'https://www.zhihu.com/billboard'
    url_weibo = 'https://weibo.com/ajax/side/hotSearch'
    url_bilibili = "https://api.bilibili.com/x/web-interface/ranking"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Cookie': ''}

    baidu = get_data_baidu(url_baidu, headers)
    zhihu = get_data_zhihu(url_zhihu, headers)
    weibo = get_data_weibo(url_weibo, headers)
    bilibili = get_data_bilibili(url_bilibili, headers)

    result = {"baidu": baidu, "zhihu": zhihu, "weibo": weibo, "bilibili": bilibili}
    with open("content.json", "w") as f:
        f.write("var data = ")
        f.write(json.dumps(result, indent=4))




if __name__ == '__main__':
    main()
