# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import book_scrapy


class TutorialItem(book_scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DmozItem(book_scrapy.Item):
    title = book_scrapy.Field()
    link = book_scrapy.Field()
    desc = book_scrapy.Field()


class TorrentItem(book_scrapy.Item):
    url = book_scrapy.Field()
    name = book_scrapy.Field()
    description = book_scrapy.Field()
    size = book_scrapy.Field()


class DoubanItem(book_scrapy.Item):
    title = book_scrapy.Field()
    href = book_scrapy.Field()
    topic_id = book_scrapy.Field()
    group_id = book_scrapy.Field()
    author_id = book_scrapy.Field()
    author_name = book_scrapy.Field()
    answer_count = book_scrapy.Field()
    last_answer_time = book_scrapy.Field()  # 最后回复的时间
    scrapy_at = book_scrapy.Field()  # 抓取的时间


    # 下面来自于详细页
    content = book_scrapy.Field()
