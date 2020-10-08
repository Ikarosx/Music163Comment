# -*- coding: utf-8 -*-
import scrapy
import re
import time
from binascii import hexlify
import os
from Crypto.Cipher import AES
import base64
import json
from Music163Spider import items


class HotcommentSpider(scrapy.Spider):
    name = 'HotComment'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/discover']
    domain = 'https://music.163.com'

    # 过滤掉无效的href
    def filterHref(self, url):
        return not (url == '#' or url.startswith('javascript'))

    def parse(self, response):
        # 找出所有a链接
        hrefs = list(
            filter(self.filterHref, response.css('a::attr(href)').extract()))
        for href in hrefs:
            match = re.match('/song\?id=([0-9a-zA-Z]+)', href)
            if(match):
                songId = match.group(1)
                # self.logger.info('歌曲ID %s' % songId)
                # 构造d，即json串
                data = '{"rid":"R_SO_4_%s","threadId":"R_SO_4_%s","pageNo":"1","pageSize":"10","cursor":"%s","offset":"0","orderType":"1","csrf_token":""}' % (
                    songId, songId, round(time.time()*1000))
                # 获取热评的api 
                nextPage = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
                # formdata携带参数
                yield scrapy.FormRequest(url=nextPage, formdata=Encrypyed().encrypt(data), callback=self.parseSong, meta={'songId': songId})
            else:
                # 拼接url
                nextPage = response.urljoin(href)
                # 只递归这几个字符串开头的链接
                if href.startswith('/artist') or href.startswith('/discover') or href.startswith('/playlist') or href.startswith('/album'):
                    # self.logger.info('访问 %s' % nextPage)
                    yield scrapy.Request(url=nextPage, callback=self.parse)

    # 解析热评
    def parseSong(self, response):
        jsonResult = json.loads(response.text)
        data = jsonResult['data']
        # 判非法
        if 'hotComments' not in data:
            return
        # 获取热评
        hotComments = data['hotComments']
        # 判非法
        if hotComments is None:
            return
        for hotComment in hotComments:
            # 获取到需要的数据
            content = hotComment['content']
            likedCount = hotComment['likedCount']
            time = hotComment['time']
            commentId = hotComment['commentId']
            replyCount = hotComment['showFloorComment']['replyCount']
            user = hotComment['user']
            userId = user.get('userId', '')
            avatarUrl = user.get('avatarUrl', '')
            nickname = user.get('nickname', '')
            songId = response.meta['songId']
            # 构建出item
            yield items.HotCommentItem(
                content=content,
                likedCount=likedCount,
                time=time,
                commentId=commentId,
                replyCount=replyCount,
                userId=userId,
                avatarUrl=avatarUrl,
                nickname=nickname,
                songId=songId
            )


# 加密类
class Encrypyed():
    def __init__(self):
        # 三个固定值，通过浏览器断点可以获得
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'

    # size位随机字符串
    def rand_char(self, size):
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    # aes加密 
    def aes_encrypt(self, text, key):
        iv = b'0102030405060708'
        # 补位
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        text = text.encode('utf-8')
        encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

        result = encryptor.encrypt(text)
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    # rsa加密
    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(hexlify(text.encode('utf-8')), 16),
                 int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def encrypt(self, text):
        i = self.rand_char(16)
        # 模拟js代码
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        return data
