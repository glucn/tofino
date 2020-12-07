import logging
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup

import config
from app.scraper.base_scraper import BaseScraperWorker


class LinkedInJobSearchResultScraper(BaseScraperWorker):
    """ Scrape LinkedIn's job search result page """

    def __init__(self):
        sleep_seconds = 3600  # 1H
        super().__init__('LinkedInJobSearchResultScraper', config.LINKEDIN_JOB_SEARCH_RESULT_SQS_QUEUE_URL, sleep_seconds)

    @classmethod
    def _remove_queries(cls, url: str):
        uu = urlparse(url)
        return urlunparse(uu._replace(query=''))

    def _scrape(self, file: str):
        soup = BeautifulSoup(file, 'html.parser')
        urls = [self._remove_queries(x['href']) for x in soup.find_all('a', class_='result-card__full-card-link')]

        for url in urls:
            logging.info(f'[LinkedInJobSearchResultScraper] Sending message for URL "{url}"')
            # TODO: send message in the SQS queue

