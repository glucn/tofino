import logging
import uuid
from datetime import datetime
from io import BytesIO

import config
from app.aws.s3 import S3
from app.crawler.base_crawler import BaseCrawlerWorker


class IndeedJobSearchResultCrawler(BaseCrawlerWorker):
    """ Crawl Indeed's job search result page """

    _SOURCE = 'ca.indeed.com'

    def __init__(self):
        super().__init__('IndeedJobSearchResultCrawler',
                         config.CRAWLER_INDEED_JOB_SEARCH_RESULT_SQS_QUEUE_URL,
                         config.BUCKET_INDEED_JOB_SEARCH_RESULT)

    def _should_crawl(self, url: str) -> bool:
        return True

    def _process_response(self, origin_url: str, final_url: str, content: str):
        file_key = f'{datetime.now().strftime("%Y-%m-%d")}-{str(uuid.uuid4())}'
        logging.info(f'[{self._worker_name}] Uploading file to "{self._upload_bucket}/{file_key}"...')
        S3.upload_file_obj(BytesIO(content.encode('utf-8')), self._upload_bucket, file_key)
        logging.info(f'[{self._worker_name}] Uploaded file to "{self._upload_bucket}/{file_key}"')
