# 爬取4今日热点事件排行榜
import requests
import json
from bs4 import BeautifulSoup

require = 9


def get_html_baidu(url, headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text


def get_pages_baidu(html):
    baidu = []
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all(class_="list-title")
    for i in range(len(content)):
        topic_name = content[i].get_text().strip()
        topic_url = content[i]['href'].strip()
        tmp = "<a href='{}' class='list-group-item list-group-item-action' target='blank'> <span class='float-left text-primary'>{}</span><span class='title'>{}</span> </a>".format(
            topic_url, i+1, topic_name)
        baidu.append(tmp)
        if (i >= require):
            break
    return baidu


def main():
    url_baidu = 'http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b1_c513'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    baidu_html = get_html_baidu(url_baidu, headers)
    baidu = get_pages_baidu(baidu_html)

    result = {"baidu": baidu,"zhihu": baidu,"weibo": baidu,"hupu": baidu}
    with open("content.json", "w") as f:
        f.write("var data = ")
        f.write(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
