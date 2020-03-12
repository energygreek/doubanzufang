# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


from scrapy.exceptions import DropItem
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['title_digist'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title_digist'])
            return item

import re
class InvalidGroupPipeline(object):

    def __init__(self):
        self.pattern = re.compile(u'南京|上海|北京|广州|成都|杭州') 

    def process_item(self, item, spider):
        if self._find(item['group']):
            raise DropItem("Invalid group found: %s" % item)
        else:
            return item

    def _find(self, string):
        return self.pattern.search(string)