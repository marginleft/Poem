# -*- coding: utf-8 -*-
import scrapy
import re
from Poem.items import PoemItem
from Poem.items import Poem
from ..utils import makedirs

index = 4
base_url = 'https://so.gushiwen.org'


class SummarySpider(scrapy.Spider):
    name = 'summary'
    allowed_domains = ['so.gushiwen.org']
    start_urls = []

    #           0   1   2   3  4   5   6   7    8   9   10   11  12
    list_max = [4, 12, 19, 29, 5, 252, 7, 777, 16, 81, 377, 818, 59]
    list_c = ['%e5%85%88%e7%a7%a6', '%e4%b8%a4%e6%b1%89', '%e9%ad%8f%e6%99%8b',
              '%e5%8d%97%e5%8c%97%e6%9c%9d', '%e9%9a%8b%e4%bb%a3', '%e5%94%90%e4%bb%a3',
              '%e4%ba%94%e4%bb%a3', '%e5%ae%8b%e4%bb%a3', '%e9%87%91%e6%9c%9d',
              '%e5%85%83%e4%bb%a3', '%e6%98%8e%e4%bb%a3', '%e6%b8%85%e4%bb%a3',
              '%e8%bf%91%e7%8e%b0%e4%bb%a3']
    #              0        1        2       3        4        5       6       7       8       9       10       11        12
    path_name = ['先秦', '两汉', '魏晋', '南北朝', '隋代', '唐代', '五代', '宋代', '金朝', '元代', '明代', '清代', '近现代']
    max = list_max[index]
    c = list_c[index]
    path = '../gushiwen/%s' % path_name[index].decode('utf-8')
    makedirs(path)
    for p in range(1, max + 1):
        start_urls.append('%s/authors/Default.aspx?p=%d&c=%s' % (base_url, p, c))

    def parse(self, response):
        path = '../gushiwen/%s' % response.xpath('//div[@class="son1"]/h1/text()').extract()[0]
        for sel in response.xpath('//div[@class="cont"][@style="margin-top:13px;"]'):
            item = PoemItem()
            item['path'] = path
            item['name'] = sel.xpath('p[@style="height:22px;"]/a[@target="_blank"]/b/text()').extract()[0]
            item['introduce'] = sel.xpath('p[@style=" margin:0px;"]/text()').extract()[0]
            item['link'] = '%s%s' % (base_url, sel.xpath('p[@style=" margin:0px;"]/a/@href').extract()[0])
            item['content'] = []
            yield scrapy.Request(item['link'], callback=self.parse_poem, meta={'item': item})

    def parse_poem(self, response):
        item = response.meta['item']
        # 获取总页数
        current_page = response.xpath('//div[@class="title"]/h1/span/text()').extract()[0].split('/')[0]
        current_page = int(current_page)
        pages = response.xpath('//div[@class="title"]/h1/span/text()').extract()[0].split('/')[-1].split('页')[0]
        pages = int(pages)
        print item['name'], '当前页数：', current_page
        print item['name'], '总共页数：', pages
        # 判断页数是否大于0
        if pages > 0 and current_page <= pages:
            for sel in response.xpath('//div[@class="sons"]/div[@class="cont"]'):
                title = sel.xpath('p[not(@class)]')[0].xpath('string(.)').extract()[0]
                detail = sel.xpath('div[@class="contson" and @id]')[0].xpath('string(.)').extract()[0].replace(' ', '')
                poem = Poem(title, detail)
                item['content'].append(poem)
            if current_page < pages:
                match = re.compile('\d.aspx')
                url = match.sub('%d.aspx' % (current_page + 1), item['link'])
                print item['name'], '下一页链接：', url
                yield scrapy.Request(url, callback=self.parse_poem, meta={'item': item})
            else:
                yield item
        else:
            yield item
