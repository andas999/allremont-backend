# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ToiletBowlsSpider(scrapy.Spider):
    name = "toiletBowls"

    start_urls = [
        'https://megastroy.kz/astana/market/santexnika/unitazy/'
    ]
    max_pages = 100
    rules = (Rule(LinkExtractor(allow=('\\search?page=\\d')), 'parse_start_url', follow=True),)

    def start_requests(self):
        for i in range(self.max_pages):
            yield scrapy.Request('https://megastroy.kz/astana/market/santexnika/unitazy/?page=%d' % i, callback=self.parse)


    def parse(self, response):
        raw_image_urls = response.xpath('//img/@src').extract()
        title = response.xpath('//div[@class="prodTitle"]/a/text()').extract()
        cost = response.xpath('//div[@class="prodPrice"]/span[@class="currentPrice"]/text()').re(r'[0-9].*')
        titles = []
        costs = []
        clean_image_urls = []
        for tit in title: 
            titles.append(tit)
        for cos in cost:
            costs.append(cos)
        for img_url in raw_image_urls:
            clean_image_urls.append(response.urljoin(img_url))

        for item in titles:
            yield {
                'title' : item
            }
        
        for item in costs: 
            yield {
                'cost' : item
            }
        
        for item in clean_image_urls:
            yield {
                'image_url' : item
            }