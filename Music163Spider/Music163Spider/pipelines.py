# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class HotCommentPipeline(object):
    def process_item(self, item, spider):
        # 判断是否有内容
        if item.get('content'):
            # 爬取点赞1w以上的
            if int(item.get('likedCount')) > 10000:
                print(item.get('likedCount'))
                return item
        # 丢弃 
        raise DropItem("drop 无内容")

# 去重
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['commentId'] in self.ids_seen:
            raise DropItem("Duplicate commentId found: %s" % item['commentId'])
        else:
            self.ids_seen.add(item['commentId'])
            return item

# 存储到mongodb
class MongoPipeline:

    collection_name = 'hot_comment'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # 设置在settings.py
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'music163')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

