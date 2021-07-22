# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class CarpetProductsSpider(scrapy.Spider):
    name = "carpetProducts"

    start_urls = [
        'https://megastroy.kz/astana/market/napolnye-pokrytiya/kovrovye-izdeliya/'
    ]
    max_pages = 100
    rules = (Rule(LinkExtractor(allow=('\\search?page=\\d')), 'parse_start_url', follow=True),)

    custom_settings = {
        'FEED_URI' : 'dataset/carpetProducts.csv'
    }

    def start_requests(self):
        for i in range(self.max_pages):
            yield scrapy.Request('https://megastroy.kz/astana/market/napolnye-pokrytiya/kovrovye-izdeliya/?page=%d' % i, callback=self.parse)


    def parse(self, response):
        response.selector.remove_namespaces()

        #Extract carpetProducts information
        titles =  response.xpath('//div[@class="prodTitle"]/a/text()').extract()
        prices = response.xpath('//div[@class="prodPrice"]/span[@class="currentPrice"]/text()').re(r'[0-9].*')
        image_urls = response.xpath('//img/@src').extract()

        for item in zip(titles,prices,image_urls):
            scraped_info = {
                'title' : item[0],
                'price' : item[1],
                'image_url' : item[2],
            }

            yield scraped_info