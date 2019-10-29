import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
import os

"""爬取猫眼Top100电影信息"""

myheader = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: __mta=51279638.1572248686868.1572248801427.1572249213031.6; uuid_n_v=v1; uuid=CF557A20F95611E9B91961B34FBA37ADE224594D0C8A4EA9947079EBFAB998F5; _csrf=b6504e58833a1439cc32f5a84a70dfd02b58f1749ef62d9533460a1a89221e2d; __mta=51279638.1572248686868.1572248693495.1572248798283.4
Host: maoyan.com
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}


def get_one_page(url):
    # print("get_one_page")
    try:
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print(RequestException.errno)
        return None


def parse_one_page(html):
    # print("parse_one_page")
    patterns = re.compile('<dd>.*?(\d+)</i>.*?title="(.*?)".*?alt.*?class.*?src="(.*?)"'
                          '.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?score.*?integer">(.*?)</i>'
                          '.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(patterns, html)
    # print(items)
    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'image': item[2],
            'actors': item[3].strip(),
            'time': item[4].strip(),
            'score': item[5] + item[6]
        }


# urllist: https://maoyan.com/board/4?offset=0(10,20,30....90)
def _main(offset):
    # print("_main")
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        store_to_file(item)
        store_jpeg(item["image"], item["title"])
        # print(item)


def store_jpeg(pic_url, title):
    response = requests.get(pic_url, headers=headers)
    if response.status_code == 200:
        with open("pics/" + title + ".jpg", "wb") as f:
            f.write(response.content)
            f.close()


def store_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    # for offset in range(10):
    #   _main(offset*10)
    os.mkdir('pics');
    pool = Pool()
    pool.map(_main, [i * 10 for i in range(10)])
