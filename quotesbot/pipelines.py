# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
import logging
from quotesbot.items import QuotesItem, AuthorItem

logger = logging.getLogger(__name__)


class QuotesbotPipeline(object):
    def process_item(self, item, spider):
        logger.debug(item)
        return item


class FilePipeline(object):
    # process_item(self, item, spider)
    # open_spider(self, spider)
    # close_spider(self, spider)
    # from_crawler(cls, crawler)
    def __init__(self):
        self.quote_file = open('quote.json', 'w')
        self.author_file = open('author.json', 'w')
        self.quote_count = 0
        self.author_count = 0

    def process_item(self, item, spider):
        self.process_author_item(item)
        self.process_quote_item(item)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.quote_file.close()

    def process_author_item(self, item):
        if not isinstance(item, AuthorItem):
            return
        self.author_count += 1
        self.author_file.write(json.dumps(dict(item)) + "\n")

    def process_quote_item(self, item):
        if not isinstance(item, QuotesItem):
            return
        self.quote_count += 1
        self.quote_file.write(json.dumps(dict(item)) + "\n")



class MongoPipeline(object):
    collection_name = 'quotesd'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
