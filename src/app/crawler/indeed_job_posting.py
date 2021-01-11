import logging
from io import BytesIO
from urllib.parse import urlparse, parse_qs

import config
from app.aws.s3 import S3
from app.crawler.base_crawler import BaseCrawlerWorker
from app.db_operator.mysql_client import MySQLClient
from app.exceptions import RetryableException
from app.models.job_posting import JobPosting


class IndeedJobPostingCrawler(BaseCrawlerWorker):
    """ Crawl Indeed's job posting page """

    _SOURCE = 'ca.indeed.com'

    def __init__(self):
        super().__init__('IndeedJobPostingCrawler',
                         config.CRAWLER_INDEED_JOB_POSTING_SQS_QUEUE_URL,
                         config.BUCKET_INDEED_JOB_POSTING,
                         60)

    def _should_crawl(self, url: str) -> bool:
        session = MySQLClient.get_session()
        existing = JobPosting.get_by_origin_url(session, url)
        session.close()

        if existing:
            logging.info(f'[{self._worker_name}] The Job Posting of {url} already exist, skipping...')
            return False

        return True

    def _process_response(self, origin_url: str, final_url: str, content: str):
        if bool(urlparse(final_url).netloc) and 'indeed' not in final_url:
            logging.warning(
                f'[{self._worker_name}] The crawler is redirected to unsupported URL {final_url}, discarding...')
            return

        source = self._SOURCE
        external_id = self._parse_external_id(final_url)

        if not external_id:
            logging.warning(
                f'[{self._worker_name}] Cannot determine external ID from the URL {final_url}, discarding...')
            return

        session = MySQLClient.get_session()
        try:
            existing = JobPosting.get_by_external_id(session=session, source=source, external_id=external_id)
            if existing:
                # TODO: consider updating existing record?
                logging.info(
                    f'[{self._worker_name}] JobPosting record with source "{source}" external_id "{external_id}" already exists')
                return

            job_posting = JobPosting.create(
                session=session,
                source=source,
                external_id=external_id,
                url=final_url,
                origin_url=origin_url,
            )

            file_key = job_posting.id
            logging.info(f'[{self._worker_name}] Uploading file to "{self._upload_bucket}/{file_key}"...')
            S3.upload_file_obj(BytesIO(content.encode('utf-8')), self._upload_bucket, file_key)
            logging.info(f'[{self._worker_name}] Uploaded file to "{self._upload_bucket}/{file_key}"')

            session.commit()
            logging.info(f'[{self._worker_name}] Created JobPosting record {job_posting.id}')

        except Exception as ex:
            logging.error(f'[{self._worker_name}] Error processing, rolling back...', ex)
            session.rollback()
            raise RetryableException
        except:
            logging.error(f'[{self._worker_name}] Unexpected exception, rolling back...')
            session.rollback()
            raise RetryableException
        finally:
            session.close()

    @staticmethod
    def _parse_external_id(url: str) -> str:
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)
        if 'jk' in queries:
            return queries['jk'][0]
        return ''
