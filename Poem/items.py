# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PoemItem(scrapy.Item):
    # define the fields for your item here like:
    path = scrapy.Field()
    name = scrapy.Field()
    introduce = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()

    def __str__(self):
        list = self['content']
        content = ''
        for poem in list:
            content += str(poem)
        if content == '':
            content = '无记录'
        return 'name : %s\nintroduce : %s\nlink : %s\n\n%s' % (self['name'], self['introduce'], self['link'], content)


class Poem:

    def __init__(self, title, detail):
        self.title = title
        self.detail = detail

    def __str__(self):
        return '%s\n%s\n' % (self.title, self.detail)
