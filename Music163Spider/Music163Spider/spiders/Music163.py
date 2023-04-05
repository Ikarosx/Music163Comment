# -*- coding: utf-8 -*-
import datetime

import re
from binascii import hexlify
import os
from Crypto.Cipher import AES
import base64
import json
import time

from .. import items
import scrapy


class Music163Spider(scrapy.Spider):
    name = 'Music163'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/discover']
    domain = 'https://music.163.com'

    # URL
    COMMENT_Url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    LYRIC_URL = 'https://music.163.com/weapi/song/lyric?csrf_token='
    SONG_DETAIL_URL = 'https://music.163.com/weapi/v3/song/detail?csrf_token='
    DOWNLOAD_SONG_URL = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    GET_PLAYLIST_DETAILS = 'https://music.163.com/weapi/v6/playlist/detail?csrf_token='
    # MV页
    MV_VIEW_URL = 'https://music.163.com/mv?id=%s'
    # 专辑页
    ALBUM_VIEW_URL = 'https://music.163.com/album?id=%s'
    # 歌手页
    ARTIST_VIEW_URL = 'https://music.163.com/artist?id=%s'

    # 过滤掉无效的href
    def filterHrefs(self, hrefs):
        notContains = ['download', '.exe', '.apk', 'javascript', '${', 'microsoft', '/sns/authorize',
                       'reg.163.com', 'official-terms', '.png', 'p5.music', 'beian', 'st/userbasic',
                       'web/reward', 'web-amped', 'uservideo#', 'apple.com', '/wiki/', 'registerSystemInfo']
        notEquals = ['', '#']
        hrefs = list(filter(lambda x: not any([text in x for text in notContains]) and not any([text == x for text in notEquals]), hrefs))
        return hrefs

    def parse(self, response):
        # 找出所有a链接，并过滤无效的
        hrefs = self.filterHrefs(response.css('a::attr(href)').extract())
        yield from self.dealResponse(response)
        if response.meta['depth'] and response.meta['depth'] > 8:
            return
        for href in hrefs:
            nextPage = response.urljoin(href)
            if 'http' not in nextPage:
                continue
            yield scrapy.Request(url=nextPage, callback=self.parse, dont_filter=False)


    # 根据请求的url和响应处理不同的逻辑
    def dealResponse(self, response):
        self.logger.info("解析" + response.url)
        href = response.url
        # 匹配歌曲
        songMatch = re.search('/song\?id=([0-9a-zA-Z]+)', href)
        if songMatch:
            self.logger.info("匹配歌曲")
            yield from self.parseSongView(response, songMatch.group(1))
        # # 匹配歌手，歌手页由于都是a链接，直接遍历即可
        # artistMatch = re.search('/artist\?id=([0-9a-zA-Z]+)', href)
        # if artistMatch:
        #     self.parseArtistView(response, artistMatch.group(1))
        #     return
        # 匹配电台
        djradioMatch = re.search('/djradio\?id=([0-9a-zA-Z]+)', href)
        if djradioMatch:
            self.logger.info("匹配电台")
            yield from self.parseDJRadioView(response, djradioMatch.group(1))
        # 匹配电台节目
        programMatch = re.search('/program\?id=([0-9a-zA-Z]+)', href)
        if programMatch:
            self.logger.info("匹配电台节目")
            yield from self.parseProgramView(response, programMatch.group(1))
        # 匹配专辑
        artistAlbumMatch = re.search('(?<!artist)/album\?id=([0-9a-zA-Z]+)', href)
        if artistAlbumMatch:
            self.logger.info("匹配专辑")
            yield from self.parseArtistAlbumView(response, artistAlbumMatch.group(1))
        # 匹配mv
        artistMvMatch = re.search('(?<!artist)/mv\?id=([0-9a-zA-Z]+)', href)
        if artistMvMatch:
            self.logger.info("匹配MV")
            yield from self.parseArtistMvView(response, artistMvMatch.group(1))
        # 匹配用户
        userMatch = re.search('/user/home\?id=([0-9a-zA-Z]+)', href)
        if userMatch:
            self.logger.info("匹配用户")
            yield from self.parseUserView(response, userMatch.group(1))
        # 歌单
        playListMatch = re.search('/playlist\?id=([0-9a-zA-Z]+)', href)
        if playListMatch:
            self.logger.info("匹配歌单")
            yield from self.parsePlayListView(response, playListMatch.group(1))
        # self.logger.info("啥都不匹配")


    def getSongItemFromResponse(self, response):
        songItem = items.MSongItem()
        songItem['id'] = re.search('/song\?id=([0-9a-zA-Z]+)', response.url).group(1)
        songItem['song_name'] = response.css(
            "body > div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > div.hd > div > em::text").extract_first()
        songItem['artist_name'] = response.css(
            "body > div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > p:nth-child(2) > span > a::text").extract_first()
        artist_id = response.css(
            "body > div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > p:nth-child(2) > span > a::attr(href)").extract_first()
        if artist_id is not None:
            songItem['artist_id'] = artist_id.split("=")[1]
        songItem['duration'] = response.css("head > meta[property='music:duration']::attr(content)").extract_first()
        # 下载url需要请求新的地址
        mv_id = response.css(
            "body > div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > div.hd > div > a::attr(href)").extract_first()
        if mv_id:
            songItem['mv_id'] = mv_id.split("=")[1]
        # 匹配发行日期
        pubDateMatcher = re.search('pubDate".*(\d{4}-\d{2}-\d{2})', response.text, re.M)
        if pubDateMatcher:
            songItem['publish_time'] = pubDateMatcher.group(1)
        album_id = response.css(
            "body > div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > p:nth-child(3) > a::attr(href)").extract_first()
        if album_id:
            songItem['album_id'] = album_id.split("=")[1]

        return songItem


    def parseSongView(self, response, songId):
        self.logger.info('解析歌曲页面，歌曲ID： %s' % songId)
        songName = response.css("head > meta[property='og:title']::attr(content)").extract_first()
        # 爬取歌曲基本信息
        vip = response.css('body > div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > div.hd.vip-song > i').extract_first() is not None
        # 热评
        # 构造d，即json串
        data = '{"rid":"R_SO_4_%s","threadId":"R_SO_4_%s","pageNo":"1","pageSize":"10","cursor":"%s","offset":"0","orderType":"1","csrf_token":""}' % (
            songId, songId, round(time.time() * 1000))
        self.logger.info("yield 热评")
        yield scrapy.FormRequest(url=self.COMMENT_Url, formdata=Encrypyed().encrypt(data),
                                 callback=self.parseComment,
                                 meta={'id': songId, 'type': 0, 'name': songName}, dont_filter=True)
        # 歌词
        data = {}
        data['lv'] = -1
        data['tv'] = -1
        data['id'] = songId
        yield scrapy.FormRequest(url=self.LYRIC_URL,
                                 formdata=Encrypyed().encrypt(json.dumps(data)), callback=self.downloadLyric,
                                 meta={'id': songId, 'songName': songName}, dont_filter=True)

        # 返回一个item
        songItem = self.getSongItemFromResponse(response)
        yield songItem

        # 只有不是vip的歌曲才可以获取下载地址
        if not vip:
            # 下载歌曲
            data = {}
            data['ids'] = [songId]
            data['level'] = 'standard'
            data['encodeType'] = 'aac'
            yield scrapy.FormRequest(url=self.DOWNLOAD_SONG_URL,
                                     formdata=Encrypyed().encrypt(json.dumps(data)), callback=self.downloadSong,
                                     meta={'id': songId}, dont_filter=True)



        # # 歌曲详情
        # data = {}
        # c = [{'id': songId}]
        # data['c'] = json.dumps(c)
        # data['id'] = songId
        # yield scrapy.FormRequest(url=self.SONG_DETAIL_URL, formdata=Encrypyed().encrypt(json.dumps(data)), callback=self.parseSongDetails,
        #                          meta={'id': songId, 'vip': vip}, dont_filter=False)

    # 解析歌词
    def downloadLyric(self, response):
        self.logger.info('解析歌词')
        jsonResult = json.loads(response.text)
        songId = response.meta['id']
        songName = response.meta['songName']
        if 'lrc' not in jsonResult:
            self.logger.warn("歌曲%s没有歌词" % songId)
            return
        lyricItem = items.MLyricItem()
        if 'lyricUser' in jsonResult:
            lyricUser = jsonResult['lyricUser']
            lyricItem['lyric_person_id'] = lyricUser['id']
            lyricItem['lyric_person_name'] = lyricUser['nickname']
        if 'transUser' in jsonResult:
            transUser = jsonResult['transUser']
            lyricItem['trans_person_id'] = transUser['id']
            lyricItem['trans_person_name'] = transUser['nickname']

        lyricItem['lrc'] = jsonResult['lrc']['lyric']
        lyricItem['lrc_version'] = jsonResult['lrc']['version']
        if 'tlyric' in jsonResult:
            lyricItem['tlrc'] = jsonResult['tlyric']['lyric']
            lyricItem['tlrc_version'] = jsonResult['tlyric']['version']
        lyricItem['song_id'] = songId
        lyricItem['song_name'] = songName
        yield lyricItem

    # 解析下载歌曲
    def downloadSong(self, response):
        self.logger.info('解析下载歌曲')
        jsonResult = json.loads(response.text)
        if 'data' not in jsonResult:
            return
        songDetails = jsonResult['data'][0]
        songUrlItem = items.MSongUrlItem()
        songUrlItem['id'] = songDetails['id']
        songUrlItem['url'] = songDetails['url']
        yield songUrlItem

    # 解析热评
    def parseComment(self, response):
        jsonResult = json.loads(response.text)
        self.logger.info("解析评论")
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
            commentItem = items.MCommentItem()
            # 获取到需要的数据
            commentItem['content'] = hotComment['content']
            commentItem['liked_count'] = hotComment['likedCount']
            createTime = hotComment['time']
            if createTime is not None:
                commentItem['create_day'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(createTime/1000))
            commentItem['id'] = hotComment['commentId']
            user = hotComment['user']
            commentItem['person_id'] = user.get('userId', '')
            commentItem['person_url'] = user.get('avatarUrl', '')
            commentItem['person_name'] = user.get('nickname', '')
            commentItem['target_id'] = response.meta['id']
            commentItem['target_name'] = response.meta['name']
            commentItem['type'] = response.meta['type']
            # 构建出item
            yield commentItem

    # 解析专辑
    def parseArtistAlbumView(self, response, albumId):
        self.logger.info("解析专辑页面：%s" % (albumId))
        albumItem = items.MAlbumItem()
        albumItem['id'] = albumId
        albumItem['album_name'] = response.css("body > div.g-bd4.f-cb.p-share > div.g-mn4 > div > div > div.m-info.f-cb > div.cnt > div > div.topblk > div > div > h2::text").extract_first()
        albumItem['publish_time'] = response.css("head > meta[property='music:release_date']::attr(content)").extract_first()
        publish_company = response.css("body > div.g-bd4.f-cb.p-share > div.g-mn4 > div > div > div.m-info.f-cb > div.cnt > div > div.topblk > p:nth-child(4)::text").extract_first()
        if publish_company:
            albumItem['publish_company'] = publish_company.strip()
        yield albumItem

    def parseArtistMvView(self, response, mvId):
        self.logger.info("解析MV页面：%s" % (mvId))
        mvItem = items.MMvItem()
        mvItem['id'] = mvId
        mvItem['mv_name'] = response.css("head > meta[property='og:title']::attr(content)").extract_first()
        mvItem['image_url'] = response.css("head > meta[property='og:image']::attr(content)").extract_first()
        mvItem['video_url'] = response.css("head > meta[property='og:video']::attr(content)").extract_first()
        mvItem['description'] = response.css("head > meta[property='og:description']::attr(content)").extract_first()
        mvItem['publish_date'] = response.css("head > meta[property='video:release_date']::attr(content)").extract_first()
        mvItem['duration'] = response.css("head > meta[property='video:duration']::attr(content)").extract_first()
        mvItem['liked_count'] = response.css("a[data-action='like']::attr(data-count)").extract_first()
        mvItem['sub_count'] = response.css("a[data-action='sub']::attr(data-count)").extract_first()
        mvItem['share_count'] = response.css("a[data-action='share']::attr(data-count)").extract_first()
        playMatcher = re.search("播放次数.(\d+.*?)次", response.text, re.M)
        if playMatcher:
            mvItem['play_count'] = playMatcher.group(1).replace('万', '0000')
        yield mvItem

    def parseUserView(self, response, userId):
        self.logger.info("解析用户页面: %s" % userId)
        userItem = items.MPersonItem()
        userItem['id'] = userId
        userItem['person_name'] = response.xpath('//*[@id="j-name-wrap"]/span[1]//text()').extract_first()
        userItem['person_img_url'] = response.xpath('//*[@id="ava"]/img//@src').extract_first()
        areaMatcher = re.search('所在地区：(.*?)</span>', response.text)
        if areaMatcher:
            userItem['area'] = areaMatcher.group(1)
        ageStamp = response.css("#age::attr(data-age)").extract_first()
        if ageStamp:
            if ageStamp[0] == '-':
                userItem['birthday'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(ageStamp)/1000)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                userItem['birthday'] = time.localtime(int(ageStamp) / 1000)
        # 0男1女
        userItem['gender'] = 0 if 'u-icn-01' in response.xpath('//*[@id="j-name-wrap"]/i//@class').extract_first() else 1
        userItem['event_count'] = response.xpath('//*[@id="event_count"]//text()').extract_first()
        userItem['follow_count'] = response.xpath('//*[@id="follow_count"]//text()').extract_first()
        userItem['fan_count'] = response.xpath('//*[@id="fan_count"]//text()').extract_first()
        # 0普通用户 1歌手
        userItem['user_type'] = 1 if 'tag u-icn2 u-icn2-pfv' in response.text or 'tag u-icn2 u-icn2-pfyyr' in response.text else 0
        yield userItem

    def parsePlayListView(self, response, playListId):
        self.logger.info("解析歌单页面：%s" % (playListId))
        # 获取歌单列表
        data = {}
        data['id'] = playListId
        data['n'] = 100000
        # 指定headers
        yield scrapy.FormRequest(url=self.GET_PLAYLIST_DETAILS,
                                 formdata=Encrypyed().encrypt(json.dumps(data)), callback=self.parsePlayListDetail,
                                  dont_filter=True)
        tags = response.css('.u-tag i::text').extract()
        for tag in tags:
            categoryItem = items.MCategoryItem()
            categoryItem['target_id'] = playListId
            categoryItem['label'] = tag
            categoryItem['type'] = 1
            yield categoryItem
    def parsePlayListDetail(self, response):
        jsonResult = json.loads(response.text)['playlist']
        playListItem = items.MPlaylistItem()

        playListItem['id'] = jsonResult['id']
        playListItem['playlist_name'] = jsonResult['name']
        playListItem['playlist_img_url'] = jsonResult['coverImgUrl']
        playListItem['create_user_id'] = jsonResult['creator']['userId']
        playListItem['create_user_name'] = jsonResult['creator']['nickname']
        if jsonResult['createTime'] is not None:
            timeArray = time.localtime(jsonResult['createTime'] / 1000)
            playListItem['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        playListItem['sub_count'] = jsonResult['subscribedCount']
        playListItem['share_count'] = jsonResult['shareCount']
        playListItem['comment_count'] = jsonResult['commentCount']
        playListItem['play_count'] = jsonResult['playCount']
        playListItem['description'] = jsonResult['description']
        yield playListItem
        # 处理歌单与歌曲
        trackIds = jsonResult['trackIds']
        for track in trackIds:
            songPlayListItem = items.MSongPlayListItem()
            songPlayListItem['song_id'] = track['id']
            songPlayListItem['play_list_id'] = jsonResult['id']
            # 保存歌单与歌曲关联
            yield songPlayListItem
            # 遍历歌曲
            yield scrapy.Request(url='https://music.163.com/song?id=' + str(track['id']), callback=self.parse, dont_filter=False)

    def parseDJRadioView(self, response, djRadioId):
        self.logger.info("解析电台 %s" % djRadioId)
        jsonResult = json.loads(response.css('#radio-data::text').extract_first())
        djRadioItem = items.MDjradioItem()
        djRadioItem['id'] = djRadioId
        djRadioItem['djradio_name'] = jsonResult['name']
        djRadioItem['cover_url'] = jsonResult['picUrl']
        djRadioItem['description'] = jsonResult['desc']
        djRadioItem['create_person_name'] = jsonResult['dj']['nickname']
        djRadioItem['create_person_id'] = jsonResult['dj']['userId']
        djRadioItem['sub_count'] = jsonResult['subCount']
        djRadioItem['program_count'] = jsonResult['programCount']
        djRadioItem['category_label'] = jsonResult['category']
        djRadioItem['create_day'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(jsonResult['createTime']/1000))
        yield djRadioItem

    def parseProgramView(self, response, programId):
        self.logger.info("解析电台节目 %s" % programId)
        if '你要查找的网页找不到' in response.text:
            self.logger.info("电台节目页面404")
            return
        programItem = items.MProgramItem()
        jsonResult = json.loads(re.search('program-data.*?>(.*?)</textarea>', response.text,re.M|re.S).group(1).strip())
        programItem['id'] = programId
        programItem['program_name'] = jsonResult['name']
        programItem['cover_url'] = jsonResult['coverUrl']
        programItem['play_count'] = jsonResult['listenerCount']
        programItem['liked_count'] = jsonResult['likedCount']
        programItem['duration'] = jsonResult['duration']
        programItem['djradio_id'] = jsonResult['radio']['id']
        programItem['order'] = jsonResult['serialNum']
        programItem['description'] = jsonResult['description']
        programItem['create_day'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(jsonResult['scheduledPublishTime']/1000))
        yield programItem


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
