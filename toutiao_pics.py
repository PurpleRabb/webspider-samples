# -*- coding: utf-8 -*-
import json
import re
import time
import urllib
from urllib import request
from urllib.parse import quote_plus, urlencode

import requests
from bs4 import BeautifulSoup
from requests import RequestException

"""爬取头条的图片搜索，注意header的填写，否则返回的数据不正确"""

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'tt_webid=6752825929321612804; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6752825929321612804; csrftoken=5424ba740b2859a0dfb270e07398306d; s_v_web_id=8d5958ccd068b30aea9bf86603508ab7; __tasessionId=6z1qcwupm1572328649213',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}


def get_search_result(keyword, offset):
    j_data = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': '1572315275587'
    }
    now = str(time.time())
    lists = now.split('.')
    now = lists[0] + lists[1][:2]
    j_data['timestamp'] = now
    url = 'https://www.toutiao.com/api/search/content/?'
    try:
        response = requests.get(url, params=urlencode(j_data), headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            # print(response.json())
            return response.json()
        else:
            return None
    except RequestException:
        print(RequestException.errno)
        return None


def get_pics(json):
    data = json.get('data')
    if data:
        for item in data:
            title = item.get('title')
            gallery_image_count = item.get('gallary_image_count')
            group_id = item.get('group_id')
            if gallery_image_count:
                yield {
                    "title": title,
                    "image_count": gallery_image_count,
                    "article_url": item.get('article_url'),
                    "image_list": item.get('image_list')
                }


download_header = {
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'p3.pstatp.com',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}


def download_image(item):
    j_data = {
        'aid': '24',
        'app_name': 'toutiao - web',
        'group_id': '6753103845611536909',
        'item_id': '6753103845611536909',
    }
    origin_url = "https://p3.pstatp.com/origin/pgc-image/"
    try:
        response = requests.get(item["article_url"], headers=headers)
        if response.status_code == 200:
            pattern = re.compile(r'.*?BASE_DATA.galleryInfo = .*?(.*?)</script>', re.S)
            details = re.match(pattern, response.text).group(1)
            pattern = re.compile(r'.*?gallery: JSON.parse(.*?)siblingList.*?}', re.S)
            line = re.match(pattern, details).group(1).encode('utf-8').decode('unicode_escape')
            md5pattern = re.compile(r'.*?([a-z0-9]{32}).*?')  # 匹配图片的md5
            for picname in list(set(re.findall(md5pattern, line))):  # set去重
                response = requests.get(origin_url + picname, headers=download_header)
                print(origin_url + picname)
                with open("./pics/" + picname + ".jpg", "wb") as f:
                    f.write(response.content)
                    f.close()
        else:
            return None
    except RequestException:
        print(RequestException.errno)
        return None


def main():
    print("main")
    for i in range(100):
        result_json = get_search_result("街拍", i * 20)  # offset(0,20,40...)
        for item in get_pics(result_json):
            download_image(item)


if __name__ == "__main__":
    main()
