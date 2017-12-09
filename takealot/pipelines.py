# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
from datetime import datetime

# csv file name template string
DAILY_DEALS_CSV_PATH_TEMPLATE = '/home/antalszabolcs01/{:%Y-%m-%d}_deals.csv'

class DailyDealsPipeline(object):
    """Pipe daily deals items to a specific CSV file."""
    def __init__(self):
        """Daily Deal Pipeline constructor."""
        self.file = None
        self.items = []
        self.spider = None
        self.writer = None

    def open_spider(self, spider):
        """Method to handle spider opening."""
        self.spider = spider
        csv_path = DAILY_DEALS_CSV_PATH_TEMPLATE.format(datetime.now())

        if os.path.exists(csv_path):
            # when a file already exists with the generated name
            # it means that an hourly scrapie is going on
            # so read in the whole csv and extend its headers
            with open(csv_path, 'r') as old_file:
                old_items = csv.DictReader(old_file)
                headers = old_items.fieldnames + self.create_ext_hourly_fieldnames()
                self.items = self.extend_item_fields(old_items)
        else:
            # if it doesn't exist then it is probably the first scrape of the day
            # so initialize the first csv with the original fields of the item
            headers = spider.export_fields

        self.file = open(csv_path, 'w')
        self.writer = csv.DictWriter(self.file, headers)
        self.writer.writeheader()

    def close_spider(self, spider):
        """Method to handle spider closing."""
        if self.items:
            self.writer.writerows(self.items)

        self.file.close()

    def process_item(self, item, spider):
        """Method to handle item processing."""
        if self.items:
            # hourly scrape
            extended_hourly_fieldnames = self.create_ext_hourly_fieldnames()
            for new_item in self.items:
                if new_item['id'] == item['id']:
                    # update item
                    for (ext_field, orig_field) in zip(extended_hourly_fieldnames,
                                                       spider.hourly_fields):
                        new_item[ext_field] = item[orig_field]

        else:
            # initial scrape
            self.writer.writerow(item)
        return item

    def extend_item_fields(self, items):
        """Extend items with new fields for the hourly scrape."""
        hourly_fields = self.create_hourly_fields()
        extended_items = [dict(item, **hourly_fields) for item in items]
        return extended_items

    def create_hourly_fields(self):
        """Create empty fields for the hourly data."""
        fieldnames = self.create_ext_hourly_fieldnames()
        return {fieldname: None for fieldname in fieldnames}

    def create_ext_hourly_fieldnames(self):
        """Create list of fieldnames for the hourly data."""
        iteration = datetime.now().hour - int(self.spider.start_hour)

        # the last scrape is at 23:55, this case the iteration would be
        # the same as the scrape of 23:00, so we need to increment it
        if self.spider.last_scrape:
            iteration += 1
        return ['{}_{}'.format(field, iteration) for field in self.spider.hourly_fields]
