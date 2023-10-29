import scrapy

from .base import BaseItem


class WebsiteItem(BaseItem):
    name = scrapy.Field()
    css_selector = scrapy.Field()
    categories_num = scrapy.Field()
    category_urls = scrapy.Field()
    total_categories = scrapy.Field()
