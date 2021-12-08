# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class DoubanzufangPipeline:
    def process_item(self, item, spider):
        return item


# 删除重复条目
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['title_digist'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title_digist'])
            return item


# 删除的条目
class InvalidGroupPipeline(object):

    def __init__(self):
        self.city = '深圳'

    def process_item(self, item, spider):
        if self._find(item['group']):
            return item
        else:
            raise DropItem("Useless item found: %s" % item)


    def _find(self, string):
        return self.pattern.search(string)
