# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PoemPipeline(object):

    def process_item(self, item, spider):
        path = item['path']
        name = item['name']
        with open('%s/%s' % (path, name), 'wb') as f:
            f.write(str(item))
        return item
