import json
import logging
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup

import config
from app.aws import SQS
from app.scraper.base_scraper import BaseScraperWorker


class IndeedJobSearchResultScraper(BaseScraperWorker):
    """ Scrape Indeed's job search result page """

    def __init__(self):
        super().__init__('IndeedJobSearchResultScraper', config.SCRAPER_INDEED_JOB_SEARCH_RESULT_SQS_QUEUE_URL)

    @classmethod
    def _parse_url(cls, url: str):
        uu = list(urlparse(url))
        uu[0] = 'https'  # scheme
        uu[1] = 'ca.indeed.com'  # netloc, the link in the search results page are all relative
        return urlunparse(uu)

    def _scrape(self, file: str, file_name: str):
        soup = BeautifulSoup(file, 'html.parser')
        urls = [self._parse_url(x['href']) for x in soup.find_all('a', class_='jobtitle turnstileLink')]

        for url in urls:
            logging.info(f'[IndeedJobSearchResultScraper] Sending message for URL "{url}"...')

            message = json.dumps({'url': url})
            SQS.send_message(config.CRAWLER_INDEED_JOB_POSTING_SQS_QUEUE_URL, message)
