# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    author = scrapy.Field()
    date_published = scrapy.Field()
    body = scrapy.Field()
    keywords = scrapy.Field()
    comments_url = scrapy.Field()
    comments = scrapy.Field()

class Comment(scrapy.Item):
    comment_id = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    reply_count = scrapy.Field()
    timestamp = scrapy.Field()
    reply_to_author = scrapy.Field()
    reply_to_comment = scrapy.Field()
    content = scrapy.Field()
