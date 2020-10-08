# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotCommentItem(scrapy.Item):
    # define the fields for your item here like:
    # 评论内容
    content = scrapy.Field()
    # 点赞数
    likedCount = scrapy.Field()
    # 评论ID
    commentId = scrapy.Field()
    # 评论时间
    time = scrapy.Field()
    # 回复数
    replyCount = scrapy.Field()
    # 发布人ID
    userId = scrapy.Field()
    # 发布人昵称
    nickname = scrapy.Field()
    # 发布人头像
    avatarUrl = scrapy.Field()
    # 歌曲ID
    songId = scrapy.Field()