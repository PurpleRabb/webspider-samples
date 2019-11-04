from time import sleep
from timeit import Timer
from urllib.parse import urlencode
# -*- coding: utf-8 -*-
import requests
import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["weixin"]
colletion = my_db['articles']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 无界面
# chrome_options.add_argument("--user-data-dir=F:\\test\\")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36")

browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 10)

"""爬取搜狗微信文章"""

_url = "https://weixin.sogou.com/weixin?"
keyword = "算法"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'SUV=0077ECEFB4A8FBC75D22D97186861107; sw_uuid=9606138648; ssuid=2798225523; IPLOC=CN3100; SUID=C7FBA8B42E18960A000000005D6F0B57; pgv_pvi=4576065536; pgv_si=s7131116544; ABTEST=2|1572572538|v1; SNUID=B08DDEC27673E04865F85F0677608163; weixinIndexVisited=1; LSTMV=235%2C77; LCLKINT=1907; JSESSIONID=aaa2gXknf4KyW8RuRnx4w; sct=18',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}


def search_article(keyword):
    try:
        browser.get('https://weixin.sogou.com/')
        _input = wait.until(EC.visibility_of(browser.find_element(by=By.ID, value='query')))
        _input.send_keys(keyword)  # keyword
        search = wait.until(EC.visibility_of(browser.find_element_by_class_name('swz2')))
        search.click()
        # print(browser.page_source)
    except TimeoutException:
        search_article(keyword)


def get_articles(page):
    try:
        wait.until(EC.visibility_of(browser.find_element_by_css_selector("#main > div.news-box")))
        selector = "dl:nth-child(3) > dd > a"
        links = browser.find_elements_by_css_selector(selector)
        for link in links:
            link.click()
            pages = browser.window_handles
            browser.switch_to.window(pages[1])
            browser.get(browser.current_url)
            html = browser.page_source
            parse_content(html)
            browser.close()  # 关闭当前句柄
            browser.switch_to.window(pages[0])  # 回到首页
    except TimeoutException:
        get_articles(0)


def parse_content(html):
    doc = pq(html)
    url = browser.current_url
    title = doc("#activity-name").text().strip()
    print(url)
    print(title)
    dic = {
        "url:": url,
        "title:": title
    }
    result = colletion.insert_one(dic)


def store_to_mongodb(dic):
    return


def main():
    search_article(keyword=keyword)
    get_articles(0)


if __name__ == '__main__':
    main()
