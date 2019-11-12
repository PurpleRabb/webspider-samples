# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy import Request

from zhihu_users.items import ZhihuUsersItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    start_user = 'excited-vczh'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
                      self.parse_follows)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuUsersItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follows_query,offset=0,limit=20),
                      self.parse_follows)

    def parse_follows(self, response):
        # print(response.text)
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                # print(result.get('url_token'))
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end') is False:
            next_page = results.get('paging').get('next')
            next_page = next_page.replace(r'https://www.zhihu.com/members/', r'https://www.zhihu.com/api/v4/members/')
            # print(next_page)
            yield Request(next_page, self.parse_follows)
