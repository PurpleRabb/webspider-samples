import os

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

"""根据关键字爬取百度图片"""

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 无界面
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 10)


def search_pic(keyword):
    try:
        browser.get('https://image.baidu.com/')
        _input = wait.until(EC.visibility_of(browser.find_element(by=By.ID, value='kw')))
        _input.send_keys(keyword)  # keyword
        search = wait.until(EC.visibility_of(browser.find_element_by_class_name('s_search')))
        search.click()
    except TimeoutException:
        search_pic(keyword)


def get_pic_url(page):
    try:
        wait.until(EC.visibility_of(browser.find_element(by=By.CSS_SELECTOR, value="#imgid")))
        selector = ".imglist.clearfix.pageNum" + str(page) + " .imgitem"
        html = browser.page_source
        doc = pq(html)
        for item in doc(selector).items():
            yield item.attr('data-objurl')
    except TimeoutException:
        get_pic_url()


def download_pic(pic_url):
    response = requests.get(pic_url, headers="")
    if response.status_code == 200:
        try:
            print(pic_url)
            with open(keyword+"/"+ pic_url.split('/')[-1], "wb") as f:
                f.write(response.content)
                f.close()
        except PermissionError:
            return


keyword = "美女"
if __name__ == '__main__':
    search_pic(keyword)
    try:
        os.mkdir(keyword)
    except FileExistsError:
        print("dir exists")
    for page in range(10):
        js = "var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)  # 触发滚动
        for item in get_pic_url(page):
            download_pic(item)
