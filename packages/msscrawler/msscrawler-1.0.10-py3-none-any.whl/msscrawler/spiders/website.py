from ..items.website_item import WebsiteItem
from .base import BaseSpider


class WebsiteSpider(BaseSpider):
    instance = "website"

    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def get_new_item_instance():
        return WebsiteItem()

    def set_default_value(self):
        items = super().set_default_value()
        items["name"] = ""  # update when error
        items["css_selector"] = ""
        items["categories_num"] = []
        items["total_categories"] = 0  # update when error

        # use in pipeline to create categories and send message
        items["category_urls"] = []
        return items
