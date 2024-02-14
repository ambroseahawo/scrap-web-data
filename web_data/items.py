# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()
    title = scrapy.Field()
    sub_heading = scrapy.Field()
    button_link = scrapy.Field()
    hero_image_link = scrapy.Field()
    testimonials = scrapy.Field()
    description = scrapy.Field()
    gallery_images = scrapy.Field()
    map_link = scrapy.Field()
    telephone = scrapy.Field()
    contact = scrapy.Field()
    directions_link = scrapy.Field()
    address_details = scrapy.Field()
    business_hours = scrapy.Field()
