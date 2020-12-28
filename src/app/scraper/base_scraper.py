import json
import logging
import sys
import time
from typing import Optional
from urllib.parse import unquote_plus

from app.aws import SQS
from app.aws.s3 import S3
from app.aws.sqs import Message
from app.exceptions.exceptions import RetryableException, NotRetryableException, MalFormedMessageException


class BaseScraperWorker:
    """ Base scraper worker """
    _is_running = False
    _worker_name: str
    _sleep_seconds: int
    _queue_url: str

    def __init__(self, worker_name: str, queue_url: str, sleep_seconds: int = 60):
        self._worker_name = worker_name
        self._queue_url = queue_url
        self._sleep_seconds = sleep_seconds

    def run(self):
        logging.info(f'[{self._worker_name}] Worker starts')
        self._is_running = True

        while self._is_running:
            logging.info(f'[{self._worker_name}] Polling message...')
            message = self._poll_message()
            if message:
                try:
                    self._process_message(message)
                    logging.info(f'[{self._worker_name}] Deleting message {message}...')
                    self._delete_message(message.receipt_handle)
                except RetryableException as ex:
                    logging.error(f'[{self._worker_name}] Got RetryableException', ex)
                except NotRetryableException as ex:
                    logging.error(f'[{self._worker_name}] Got NotRetryableException', ex)
                    logging.info(f'[{self._worker_name}] Deleting message {message}...')
                    self._delete_message(message.receipt_handle)
                except:
                    logging.error(f'[{self._worker_name}] Got unexpected exception', sys.exc_info()[0])
            else:
                logging.info(f'[{self._worker_name}] No message received')

            time.sleep(self._sleep_seconds)

        logging.info(f'[{self._worker_name}] Worker stops')

    def _process_message(self, message: Message):
        logging.info(f'[{self._worker_name}] Received message {message}')
        bucket_name, object_key = self._parse_message(message.body)

        logging.info(f'[{self._worker_name}] Downloading file from bucket "{bucket_name}", object key "{object_key}"...')
        file_str = S3.download_file_str(bucket_name, object_key)

        logging.info(f'[{self._worker_name}] Scraping file...')
        self._scrape(file_str)

    def _poll_message(self) -> Optional[Message]:
        messages = SQS.receive_message(self._queue_url, 1)
        if len(messages) == 1:
            return messages[0]
        elif len(messages) > 1:
            raise Exception(f'[{self._worker_name}] Polling for maximum 1 message, but got {messages}')
        else:
            return None

    def _delete_message(self, receipt_handle):
        SQS.delete_message(self._queue_url, receipt_handle)

    def _parse_message(self, message_body: str) -> (str, str):
        """
        Parse the S3 notification message to get the bucket name and object key
        https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html
        """
        body_obj = json.loads(message_body)
        if 'Records' not in body_obj or len(body_obj['Records']) == 0 or len(body_obj['Records']) > 1:
            raise MalFormedMessageException(f'Message {message_body} is malformed')

        record = body_obj['Records'][0]

        if 's3' not in record or 'bucket' not in record['s3'] or 'name' not in record['s3']['bucket'] \
                or 'object' not in record['s3'] or 'key' not in record['s3']['object']:
            raise MalFormedMessageException(f'Record {record} is malformed')

        return record['s3']['bucket']['name'], unquote_plus(record['s3']['object']['key'])

    def _scrape(self, file: str):
        pass
