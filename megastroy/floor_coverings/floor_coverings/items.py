# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class SubMaterialItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    available_amount = scrapy.Field()
    description = scrapy.Field()
    material_id = scrapy.Field()