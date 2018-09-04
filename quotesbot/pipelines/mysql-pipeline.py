import json
import logging
from quotesbot.items import QuotesItem, AuthorItem
from twisted.enterprise import adbapi
import pymysql.cursors


logger = logging.getLogger(__name__)


class MysqlPipeline(object):
    database = 'quotes'
    quote_count = 0

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            port=settings["MYSQL_PORT"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            db=settings["MYSQL_DB"],
            use_unicode=True,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        return cls(
            dbpool=adbapi.ConnectionPool("pymysql", **dbparms)
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if self.process_quote_item(item):
            self.quote_count += 1
        return item

    def handle_error(self, failure):
        if failure is not None:
            logger.error(failure)

    def process_quote_item(self, item):
        if not isinstance(item, QuotesItem):
            return False
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addCallback(self.handle_error)
        return True

    def do_insert(self, cursor, item):
        insert_sql = """
            INSERT INTO quotes(author, tags, text)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_sql, (item['author'], json.dumps(item['tags']), item['text']))
