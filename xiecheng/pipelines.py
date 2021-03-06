# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from xiecheng.items import Xiechengitem

import pymongo

class XiechengPipeline(object):
    def process_item(self, item, spider):


        return item


class mongopipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_uri=mongo_url
        self.mongo_db=mongo_db


    @classmethod
    def from_crawler(cls,crawler):
        return cls (
            mongo_url=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].update({'id': item.get('nameid')}, {'$set': dict(item)}, True)
        return item



