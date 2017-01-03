# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import logging

import pymongo
from book_scrapy.exceptions import DropItem

import settings
from utility.util_decorator import check_spider_pipeline
from utility.util_string import JsonEncoder


# 一个pipeline示例
class PricePipeline(object):
    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)


# 将数据保存到json文件
class JsonWithEncodingPipeline(object):
    def __init__(self):
        logging.info(self.__dict__)
        self.file = codecs.open('zufang.json', 'w', encoding='utf-8')

    @check_spider_pipeline
    def process_item(self, item, spider):
        line = json.dumps(dict(item), cls=JsonEncoder, ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 将数据保存到MongoDB
class MongodbStorePipeline(object):
    # http://www.open-open.com/lib/view/open1414223469247.html
    # www.cnblogs.com/tk091/p/3673984.html

    def __init__(self):
        client = pymongo.MongoClient()
        tdb = client[settings.MONGODB_DBNAME]
        self.db = tdb[settings.MONGODB_DOCNAME]  # 创建聚集
        logging.info(self.db.count())

    def process_item(self, item, spider):
        if self.db.find_one({'$or': [{'topic_id': item['topic_id']}, {'title': item['title']}]}):
            raise DropItem('item %s has exists.' % item['topic_id'])

        house = dict(item)
        self.db.insert(house)
        return item


class SqliteStorePipeLine(object):

    def __init__(self):
        client = pymongo.MongoClient()
        tdb = client[settings.MONGODB_DBNAME]
        self.db = tdb[settings.MONGODB_DOCNAME]  # 创建聚集
        logging.info(self.db.count())


    def process_item(self, item, spider):
        if self.db.find_one({'$or': [{'topic_id': item['topic_id']}, {'title': item['title']}]}):
            raise DropItem('item %s has exists.' % item['topic_id'])

        house = dict(item)
        self.db.insert(house)
        return item