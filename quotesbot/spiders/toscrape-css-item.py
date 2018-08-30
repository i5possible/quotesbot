# -*- coding: utf-8 -*-
import scrapy
from quotesbot.items import QuotesItem, AuthorItem


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css-item"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = QuotesItem({
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            })
            yield item
            author_href = quote.css("span > a::attr(href)").extract_first()
            yield scrapy.Request(url=response.urljoin(author_href), callback=self.parse_author)

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_author(self, response):
        item = AuthorItem({
            'author_name': (response.css("h3.author-title::text").extract_first()),
            'author_born_date': (response.css("span.author-born-date").extract_first()),
            'author_born_location': (response.css("span.author-born-location").extract_first()),
            'author_description': (response.css("div.author-description").extract_first())
        })
        yield item
