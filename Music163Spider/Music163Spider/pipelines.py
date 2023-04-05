# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from . import items
from sqlalchemy.orm import scoped_session
import time
import json
from sqlalchemy.ext.declarative import declarative_base
import logging
logger = logging.getLogger(__name__)

class MySQLPipeline(object):

    def __init__(self, mysql_uri):
        self.mysql_uri = mysql_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # 设置在settings.py
            mysql_uri=crawler.settings.get('MYSQL_URI')
        )

    def open_spider(self, spider):
        # 连接数据库
        # 初始化数据库连接:
        logger.info("初始化数据库连接")
        engine = create_engine(self.mysql_uri,
            pool_size=32,  # 连接池大小
            pool_timeout=30,
            pool_recycle=3600)
        # 创建DBSession类型:
        self.sessionFactory = sessionmaker(bind=engine)
        logger.info("初始化数据库连接完成")
    def close_spider(self, spider):
        logger.info("关闭爬虫")


    def process_item(self, item, spider):
        session = scoped_session(self.sessionFactory)
        logger.info("处理item: ")
        if isinstance(item, items.MAlbumItem):
            entity = items.MAlbumMysqlEntity(**item)
        elif isinstance(item, items.MCategoryItem):
            entity = items.MCategoryMysqlEntity(**item)
        elif isinstance(item, items.MCommentItem):
            entity = items.MCommentMysqlEntity(**item)
        elif isinstance(item, items.MLyricItem):
            entity = items.MLyricMysqlEntity(**item)
        elif isinstance(item, items.MMvItem):
            entity = items.MMvMysqlEntity(**item)
        elif isinstance(item, items.MPersonItem):
            entity = items.MPersonMysqlEntity(**item)
        elif isinstance(item, items.MPlaylistItem):
            entity = items.MPlaylistMysqlEntity(**item)
        elif isinstance(item, items.MSongItem):
            entity = items.MSongMysqlEntity(**item)
        elif isinstance(item, items.MSongPlayListItem):
            entity = items.MSongPlayListMysqlEntity(**item)
        elif isinstance(item, items.MDjradioItem):
            entity = items.MDjradioMysqlEntity(**item)
        elif isinstance(item, items.MProgramItem):
            entity = items.MProgramMysqlEntity(**item)
        elif isinstance(item, items.MSongUrlItem):
            try:
                # 更新
                entitys = session.query(items.MSongMysqlEntity).filter(items.MSongMysqlEntity.id == item['id'])
                if entitys is None:
                    return item
                # 取第一个值
                entity = entitys.one()
                entity.url = item['url']
                session.commit()
            except Exception as e:
                spider.logger.error(e)
                session.rollback()
            return item
        else:
            return item
        entity.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            if entity.id:
                # 如果存在直接删除
                exists = session.query(type(entity)).filter(type(entity).id == entity.id).delete()
                session.commit()
                # if exists:
                #     logger.info('id为%s的%s已经存在，先删除' % (entity.id, type(entity)))
                #     exists.delete()
            session.add(entity)
            session.commit()
        except Exception as e:
            spider.logger.error(e)
            session.rollback()
        session.remove()
        return item


class HotCommentPipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item, items.MCommentItem):
            return item
        # 判断是否有内容
        if item['content']:
            # 爬取点赞1w以上的
            if int(item['liked_count']) > 10000:
                return item
        # 丢弃 
        raise DropItem("drop 点赞不足10000")


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

