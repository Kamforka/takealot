# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
from datetime import datetime


class DefaultValuePipeline(object):
    """Default value pipeline."""

    def process_item(self, item, spider):
        """Add default values to item fields."""
        item.setdefault('date', '{:%Y-%m-%d}'.format(datetime.now()))
        item.setdefault('seller_name', None)

        return item


# csv file name template string
CSV_LOG_NAME = '{date:%Y-%m-%d}_{name}.csv'

class DailyDealsPipeline(object):
    """Pipe daily deals items to a specific CSV file."""
    @classmethod
    def from_crawler(cls, crawler):
        """Instantiate pipeline from crawler."""
        spider = crawler.spider
        export_path = crawler.settings.get('export_path', '')
        last_scrape = bool(crawler.settings.get('last', False))
        start_hour = int(crawler.settings.get('start_hour', 7))
        export_fields = spider.custom_settings.get('FEED_EXPORT_FIELDS')
        if export_fields is None:
            raise ValueError('"{}" spider has no `FEED_EXPORT_FIELDS` in its settings!'
                             .format(spider.__class__.__name__))

        hourly_fieldnames = cls.parse_hourly_fieldnames(crawler.settings.get('hourly_fields'))

        return cls(export_path=export_path, start_hour=start_hour, last_scrape=last_scrape,
                   hourly_fieldnames=hourly_fieldnames, export_fields=export_fields,)

    def __init__(self, start_hour=7, last_scrape=False, export_path='', **kwargs):
        """Daily Deal Pipeline constructor."""
        self.start_hour = start_hour
        self.last_scrape = last_scrape
        self.export_path = export_path
        self.export_fields = kwargs.get('export_fields')
        self.hourly_fieldnames = kwargs.get('hourly_fieldnames')

        for fieldname in self.hourly_fieldnames:
            if fieldname not in self.export_fields:
                raise ValueError('Hourly fieldname "{}" not found in export fields.'
                                 .format(fieldname))


        self.file = None  # csv export file
        self.items = []  # list of export items
        self.writer = None  # csv dictwriter
        self.hourly_scrape = False
        self.spider = None


    def open_spider(self, spider):
        """Method to handle spider opening."""
        self.spider = spider
        csv_path = self.create_csv_path()

        if os.path.exists(csv_path):
            # when a file already exists with the generated name
            # it means that an hourly scrape is going on
            # so read in the whole csv and extend its headers
            self.hourly_scrape = True
            with open(csv_path, 'r') as old_file:
                old_items = csv.DictReader(old_file)
                headers = old_items.fieldnames + self.create_ext_hourly_fieldnames()
                self.items = self.extend_item_fields(old_items)
        else:
            # if it doesn't exist then it is probably the first scrape of the day
            # so initialize the first csv with the original fields of the item
            headers = self.export_fields

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
                                                       self.hourly_fieldnames):
                        new_item[ext_field] = item[orig_field]

        else:
            # initial scrape
            self.items.append(item)
        return item

    @staticmethod
    def parse_hourly_fieldnames(hourly_fieldnames):
        """Parse hourly_fieldnames argument."""
        if hourly_fieldnames is None:
            return []

        return hourly_fieldnames.split(',')

    def create_csv_path(self):
        """Create CSV path string."""
        return os.path.join(self.export_path,
                            CSV_LOG_NAME.format(date=datetime.now(),
                                                name=self.spider.name))

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
        iteration = datetime.now().hour - self.start_hour

        # the last scrape is at 23:55, this case the iteration would be
        # the same as the scrape of 23:00, so we need to increment it
        if self.last_scrape:
            iteration += 1
        return ['{}_{}'.format(field, iteration) for field in self.hourly_fieldnames]

    def get_hourly_count(self, header):
        """Retrieve the next count postfix for the hourly fieldnames."""
        for fieldname in header:
            if self.hourly_fieldnames[0] in fieldname:
                try:
                    return int(fieldname.split('_')[-1]) + 1
                except ValueError:
                    return 1
