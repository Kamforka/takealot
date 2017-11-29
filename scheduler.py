"""Scheduler for spiders."""
import schedule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def crawl_job():
    """Job to start takealot spiders."""
    process = CrawlerProcess(get_project_settings())

    # 'deals' is the name of one of the spider
    process.crawl('deals')
    process.start() # the script will block here until the crawling is finished

def init_schedules():
    """Initialize schedules for jobs."""
    schedule.every(30).seconds.do(crawl_job)

if __name__ == '__main__':

    init_schedules()
    
    while True:
        schedule.run_pending()
