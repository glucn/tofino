import logging

import config
from app.scraper.base_scraper import BaseScraperWorker


class IndeedJobPostingScraper(BaseScraperWorker):
    """ Scrape Indeed's job posting page """

    def __init__(self):
        super().__init__('IndeedJobPostingScraper', config.SCRAPER_INDEED_JOB_POSTING_SQS_QUEUE_URL)

    def _scrape(self, file: str):
        # TODO: implement me
        logging.info('IndeedJobPostingScraper is scraping')
