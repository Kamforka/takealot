# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
from datetime import datetime

from takealot.settings import FEED_EXPORT_FIELDS

# csv file name template string
CSV_NAME_TEMPLATE = '{:%Y-%m-%d}_deals.csv'

# hour of first scrape
START_HOUR = 9 # 09:00

# data fields for hourly scraping
HOURLY_FIELDNAMES = ['price_offer', 'stock_remaining', 'warehouses']

    # def __init__(self):
    #     self.file = None
    #     self.writer = None
    #     self.items = []
class DailyDealsPipeline(object):

    def open_spider(self, spider):
        csv_path = CSV_NAME_TEMPLATE.format(datetime.now())

        self.items = []
        if os.path.exists(csv_path):
            # when a file already exists with the generated name
            # it means that an hourly scraping is going on
            # so read in the whole csv and extend its headers
            with open(csv_path, 'r') as old_file:
                reader = csv.DictReader(old_file)
                old_items = (item for item in reader)
                headers = reader.fieldnames + self.create_hourly_fieldnames()
                self.items = self.extend_item_fields(old_items)
        else:
            headers = FEED_EXPORT_FIELDS

        self.file = open(csv_path, 'w')
        self.writer = csv.DictWriter(self.file, headers)
        self.writer.writeheader()

    def close_spider(self, spider):
        if self.items:
            self.writer.writerows(self.items)

        self.file.close()

    def process_item(self, item, spider):
        if self.items:
            hourly_fieldnames = self.create_hourly_fieldnames()
            # hourly scrape
            for new_item in self.items:
                if new_item['id'] == item['id']:
                    # update item
                    for (f1, f2) in zip(hourly_fieldnames, HOURLY_FIELDS):
                        new_item[f1] = item[f2]
        else:
            # initial scrape
            self.writer.writerow(item)
        # self.writer.writerow(item)
        return item

    def extend_item_fields(self, old_items):
        hourly_fields = self.create_hourly_fields()
        new_items = [dict(old_item, **hourly_fields) for old_item in old_items]
        return new_items


    @staticmethod
    def create_hourly_fieldnames():
        return ['{}_1'.format(field) for field in HOURLY_FIELDS]

    @staticmethod
    def create_hourly_fields():
        return {'{}_1'.format(field): None for field in HOURLY_FIELDS}
