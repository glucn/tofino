import json
import logging
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs

from bs4 import BeautifulSoup

import config
from app.aws import SQS
from app.scraper.base_scraper import BaseScraperWorker


class IndeedJobSearchResultScraper(BaseScraperWorker):
    """ Scrape Indeed's job search result page """

    def __init__(self):
        sleep_seconds = 1800  # 30 minutes
        super().__init__('IndeedJobSearchResultScraper', config.SCRAPER_INDEED_JOB_SEARCH_RESULT_SQS_QUEUE_URL, sleep_seconds)

    @classmethod
    def _parse_url(cls, url: str):
        uu = list(urlparse(url))
        query_parameters = parse_qs(uu[4], keep_blank_values=True)
        jk = query_parameters['jk']
        uu[4] = urlencode({'jk': jk}, doseq=True)
        return urlunparse(uu)

    def _scrape(self, file: str):
        soup = BeautifulSoup(file, 'html.parser')
        urls = [self._parse_url(x['href']) for x in soup.find_all('a', class_='turnstileLink')]

        for url in urls:
            logging.info(f'[IndeedJobSearchResultScraper] Sending message for URL "{url}"...')

            message = json.dumps({'url': url})
            SQS.send_message(config.CRAWLER_INDEED_JOB_POSTING_SQS_QUEUE_URL, message)
