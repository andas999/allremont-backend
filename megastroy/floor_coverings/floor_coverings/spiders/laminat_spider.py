# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class LaminatSpider(scrapy.Spider):
    name = "laminats"

    start_urls = [
        'https://megastroy.kz/astana/market/napolnye-pokrytiya/laminat/'
    ]
    max_pages = 2
    rules = (Rule(LinkExtractor(allow=('\\search?page=\\d')), 'parse_start_url', follow=True),)

    custom_settings = {
        'FEED_URI' : 'dataset/laminats.csv'
    }

    def start_requests(self):
        for i in range(self.max_pages):
            yield scrapy.Request('https://megastroy.kz/astana/market/napolnye-pokrytiya/laminat/?page=%d' % i, callback=self.parse)


    def parse(self, response):
        response.selector.remove_namespaces()

        #Extract laminats information
        titles = response.xpath('//div[@class="prodTitle"]/a/text()').extract()
        prices = response.xpath('//div[@class="prodPrice"]/span[@class="currentPrice"]/text()').re(r'[0-9].*')
        image_urls = response.xpath('//img/@src').extract()
        available_amounts = response.xpath('//form[@class="ms2_form"]/p/text()').extract()

        for item in zip(titles, prices, image_urls, available_amounts):
            scraped_info = {
                'title': item[0],
                'price': item[1],
                'image_url': item[2],
                'available_amount': item[3],
                'material_id': 1
            }

            yield scraped_info