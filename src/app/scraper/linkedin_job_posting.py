import logging

import config
from app.scraper.base_scraper import BaseScraperWorker


class LinkedInJobPostingScraper(BaseScraperWorker):
    """ Scrape LinkedIn's job posting page """

    def __init__(self):
        super().__init__('LinkedInJobPostingScraper', config.SCRAPER_LINKEDIN_JOB_POSTING_SQS_QUEUE_URL)

    def _scrape(self, file: str, file_name: str):
        # TODO: implement me
        logging.info('LinkedInJobPostingScraper is scraping')
