#!/usr/bin/python3
"""Scheduler for spiders."""
import time

import schedule
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from takealot.spiders.deals import DealsSpider


def crawl_job():
    """Job to start takealot spiders."""
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(DealsSpider)
    deferred.addCallback(reactor.callLater, 5, crawl_job)
    return deferred


def init_schedules():
    """Initialize schedules for jobs."""
    schedule.every(20).seconds.do(crawl_job)

if __name__ == '__main__':
    crawl_job()

    reactor.run()

    # init_schedules()

    # start the twisted reactor
    # while True:
    #     schedule.run_pending()
