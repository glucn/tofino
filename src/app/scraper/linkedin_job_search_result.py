import logging

import config
from app.scraper.base_scraper import BaseScraperWorker


class LinkedInJobSearchResultScraper(BaseScraperWorker):
    """ Scrape LinkedIn's job search result page """

    def __init__(self):
        sleep_seconds = 3600  # 1H
        super().__init__('LinkedInJobSearchResultScraper', config.LINKEDIN_JOB_SEARCH_RESULT_SQS_QUEUE_URL, sleep_seconds)

    def _scrape(self, file: str):
        # TODO: implement me
        logging.info('LinkedInJobSearchResultScraper is scraping')
