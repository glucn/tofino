import json
import logging
import time
import uuid
from typing import Optional

import requests

from app.aws.s3 import S3
from app.aws.sqs import Message, SQS
from app.exceptions import RetryableException, NotRetryableException, MalFormedMessageException


class BaseCrawlerWorker:
    """ Base crawler worker  """
    _is_running = False
    _worker_name: str
    _sleep_seconds: int
    _queue_url: str
    _upload_bucket: str

    def __init__(self, worker_name: str, queue_url: str, upload_bucket: str, sleep_seconds: int = 60):
        self._worker_name = worker_name
        self._queue_url = queue_url
        self._upload_bucket = upload_bucket
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
                except RetryableException:
                    time.sleep(self._sleep_seconds)
                    continue
                except NotRetryableException as ex:
                    logging.error(ex)
                finally:
                    logging.info(f'[{self._worker_name}] Deleting message {message}...')
                    self._delete_message(message.receipt_handle)
            else:
                logging.info(f'[{self._worker_name}] No message received')

            time.sleep(self._sleep_seconds)

        logging.info(f'[{self._worker_name}] Worker stops')

    def _process_message(self, message: Message):
        logging.info(f'[{self._worker_name}] Received message {message}')
        url = self._parse_message(message.body)

        response = requests.get(url)
        if response.status_code != 200:
            logging.error(f'Getting URL "{url}" resulted in status code {response.status_code}, full response "{response}"')
            raise Exception

        file_key = str(uuid.uuid4())

        logging.info(
            f'[{self._worker_name}] Uploading file downloaded from "{url}" to bucket "{self._upload_bucket}", ' +
            'object key "{file_key}"...')
        S3.upload_file_obj(response.raw, self._upload_bucket, file_key)

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
        Parse the message
        """
        body_obj = json.loads(message_body)
        if 'url' not in body_obj:
            raise MalFormedMessageException(f'Message {message_body} is malformed')

        return body_obj['url']