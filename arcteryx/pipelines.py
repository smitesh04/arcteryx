# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from arcteryx.items import ArcteryxItem
from arcteryx.db_config import DbConfig
obj = DbConfig()


class ArcteryxPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ArcteryxItem):
            obj.insert_data_table(item)
            obj.update_store_links_status(item['url'])
        return item
