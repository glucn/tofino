import json
import logging
from typing import Optional

import requests

from app.aws.sqs import Message, SQS
from app.exceptions import RetryableException, NotRetryableException, MalFormedMessageException
from app.utils.sleep_with_jitter import sleep_with_jitter


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
                    sleep_with_jitter(self._sleep_seconds)
                    continue
                except NotRetryableException as ex:
                    logging.error(ex)
                finally:
                    logging.info(f'[{self._worker_name}] Deleting message {message}...')
                    self._delete_message(message.receipt_handle)
            else:
                logging.info(f'[{self._worker_name}] No message received')

            sleep_with_jitter(self._sleep_seconds)

        logging.info(f'[{self._worker_name}] Worker stops')

    def _poll_message(self) -> Optional[Message]:
        messages = SQS.receive_message(self._queue_url, 1)
        if len(messages) == 1:
            return messages[0]
        elif len(messages) > 1:
            raise Exception(f'[{self._worker_name}] Polling for maximum 1 message, but got {messages}')
        else:
            return None

    def _process_message(self, message: Message):
        logging.info(f'[{self._worker_name}] Received message {message}')
        url = self._parse_message(message.body)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Content-Type': 'text/html',
        }

        with requests.get(url, stream=True, allow_redirects=True, headers=headers) as response:
            if response.status_code != 200:
                logging.error(f'Getting URL "{url}" resulted in status code {response.status_code}')
                raise Exception

            logging.info(f'[{self._worker_name}] Original URL {url}, final URL {response.url}')

            logging.info(f'[{self._worker_name}] Content {response.content}')
            self._process_response(response)

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

    def _process_response(self, response: requests.Response):
        pass
