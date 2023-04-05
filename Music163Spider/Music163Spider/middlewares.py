# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time

import requests
import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import logging
import random
import aiohttp
import asyncio

from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger(__name__)
class Music163SpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)





# 代理
class ProxyMiddleware(object):

    async def process_request(self, request, spider):
        # 解决一开始的请求携带了代理
        request.meta['proxy'] = None
        # request.meta['proxy'] = await asyncio.create_task(self.getProxyIp())

    # 从代理池获取IP
    async def getProxyIp(self):
        # ipJson = requests.get("http://tencent.ikarosx.cn:5010/get/").json()
        async with aiohttp.ClientSession() as client:
            ipJson = await client.get('http://127.0.0.1:5010/get/')
            ipJson = await ipJson.json()
            # ipJson = requests.get("http://127.0.0.1:5010/get/").json()
            if 'proxy' not in ipJson:
                logger.warning("代理池没有IP，暂停10s")
                time.sleep(10)
                return await asyncio.create_task(self.getProxyIp())
            proxy = 'https://' + ipJson['proxy'] if ipJson['https'] else 'http://' + ipJson['proxy']
            # logger.info("切换代理:%s" % proxy)
            return proxy


# 随机UA头
class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('USER_AGENT_LIST')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
        return None




class Music163SpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        request.cookies = {
            "MUSIC_U": '1111'
        }
        # musicUList = ['/v6/playlist/detail', '/artist']
        # if any([text in request.url for text in musicUList]):
        #     request.cookies = {
        #         "MUSIC_U": '238ce537d3c4801fd3cea96c7a1e3bfcb545d30c01ca9f943d6e69f0b6dc293833a649814e309366'
        #     }
        # else:
        #     request.headers['Cookie'] = ''
        #     request.cookies = {
        #     }
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def dealRepeatRequests(self, request):
        if isinstance(request, scrapy.Request):
            return scrapy.Request(url=request.url, callback=request.callback, dont_filter=True, meta=request.meta)
        elif isinstance(request, scrapy.FormRequest):
            return scrapy.FormRequest(url=request.url, callback=request.callback, body=request.body, meta=request.meta, dont_filter=True)
        logger.warn("不属于任何request")
        logger.warn(type(request))
        raise IgnoreRequest

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if response.status != 200:
            spider.logger.warn("状态码为%s, url为：%s" % (response.status, request.url))
            return self.dealRepeatRequests(request)
            # return request
        if '你要查找的网页找不到' in response.text:
            # spider.logger.warn(request.headers)
            # spider.logger.warn(request.cookies)
            if 'mv?id=' in request.url:
                # 如果查找mv出现网页不存在，就真的不存在
                spider.logger.warn("mv不存在,id:%s" % request.url)
                raise IgnoreRequest
            if 'com/album?id=' in request.url:
                # 如果查找mv出现网页不存在，就真的不存在
                spider.logger.warn("专辑不存在,id:%s" % request.url)
                raise IgnoreRequest
            if 'song?id=' in request.url:
                # 歌曲不存在
                spider.logger.warn("歌曲不存在,id:%s" % request.url)
                raise IgnoreRequest
            if 'user/home' in request.url:
                # 如果查找用户信息出现网页不存在，可能是不存在，也可能需要换ip
                # TODO
                pass
            spider.logger.warn(request.headers)
            spider.logger.warn("你要查找的网页找不到，疑似请求频率过高,重新请求, %s, %s" % (request.url, request.meta['proxy'] if 'proxy' in request.meta else ''))
            return self.dealRepeatRequests(request)
        if '请稍候再试' in response.text:
            spider.logger.warn("请稍后再试，疑似请求频率过高,重新请求, %s" % request.url)
            return self.dealRepeatRequests(request)
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        spider.logger.error("请求出现异常, URL:%s" % (request.url))
        spider.logger.error(exception)
        return self.dealRepeatRequests(request)
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
