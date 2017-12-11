# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
from datetime import datetime

from takealot.spiders.deals import DealsSpider
from takealot.spiders.sunglasses import SunglassSpider


class DefaultValuePipeline(object):
    """Default value pipeline."""

    def process_item(self, item, spider):
        """Add default values to item fields."""
        item.setdefault('date', '{:%Y-%m-%d}'.format(datetime.now()))

        return item


# csv file name template string
DAILY_DEALS_CSV_PATH_TEMPLATE = '{:%Y-%m-%d}_deals.csv'

# hourly_fieldnames, last_scrape, export_path, export_fields(custom_settings),
# start_hour


class DailyDealsPipeline(object):
    """Pipe daily deals items to a specific CSV file."""
    @classmethod
    def from_crawler(cls, crawler):
        spider = crawler.spider
        export_path = crawler.settings.get('export_path', '')
        last_scrape = crawler.settings.get('last', False)
        start_hour = int(crawler.settings.get('start_hour', 7))
        hourly_fieldnames = crawler.settings.get('hourly_fieldnames', '').split(',')
        export_fields = spider.custom_settings['FEED_EXPORT_FIELDS']

        for fieldname in hourly_fieldnames:
            if not fieldname in export_fields:
                raise ValueError('Hourly fieldname "{}" not found in the export fields of {}.'
                                 .format(fieldname, spider.__name__))
        return cls()

    def __init__(self):
        """Daily Deal Pipeline constructor."""
        self.file = None  # csv export file
        self.items = []  # list of export items
        self.spider = None  # spider that utilizing the pipeline
        self.writer = None  # csv dictwriter
        self.hourly_scrape = False
        self.last_scrape = False
        self.export_path = ''

    def open_spider(self, spider):
        """Method to handle spider opening."""
        self.spider = spider
        csv_path = DAILY_DEALS_CSV_PATH_TEMPLATE.format(datetime.now())

        if os.path.exists(csv_path):
            # when a file already exists with the generated name
            # it means that an hourly scrapie is going on
            # so read in the whole csv and extend its headers
            self.hourly_scrape = True
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

    def close_spider(self, spider):
        """Method to handle spider closing."""
        if self.items:
            self.writer.writeheader()
            self.writer.writerows(self.items)

        self.file.close()

    def process_item(self, item, spider):
        """Method to handle item processing."""
        if self.hourly_scrape:
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
            self.items.append(item)
            # self.writer.writerow(item)
        return item

    def create_csv_path(self):
        """Create CSV path string."""
        return os.path.join(self.export_path,
                            DAILY_DEALS_CSV_PATH_TEMPLATE.format(datetime.now()))

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
