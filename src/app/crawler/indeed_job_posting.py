import logging
from urllib.parse import urlparse, parse_qs

import config
from app.crawler.base_crawler import BaseCrawlerWorker


class IndeedJobPostingCrawler(BaseCrawlerWorker):
    """ Crawl Indeed's job posting page """

    _SOURCE = 'ca.indeed.com'

    def __init__(self):
        super().__init__('IndeedJobPostingCrawler',
                         config.CRAWLER_INDEED_JOB_POSTING_SQS_QUEUE_URL,
                         config.BUCKET_INDEED_JOB_POSTING,
                         60)

    def _get_job_posting_source(self) -> str:
        return self._SOURCE

    def _parse_external_id(self, url: str) -> str:
        parsed_url = urlparse(url)
        jk = parse_qs(parsed_url.query)['jk']
        if len(jk) < 1:
            logging.warning(f'[{self._worker_name}] Found no "jk" query parameter in {url}, will use an empty external_id')
            return ''
        return jk[0]
