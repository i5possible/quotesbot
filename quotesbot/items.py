# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy.item
from scrapy.item import Item, Field


class QuotesbotItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuotesItem(Item):
    text = Field()
    tags = Field()
    author = Field()


class AuthorItem(Item):
    author_name = Field()
    author_born_date = Field()
    author_born_location = Field()
    author_description = Field()
