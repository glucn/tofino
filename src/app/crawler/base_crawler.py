import json
import logging
from typing import Optional

from app.aws.sqs import Message, SQS
from app.crawler.proxies_manager import ProxiesManager
from app.exceptions import RetryableException, NotRetryableException, MalFormedMessageException
from app.utils.sleep_with_jitter import sleep_with_jitter


class BaseCrawlerWorker:
    """ Base crawler worker  """
    _is_running = False
    _worker_name: str
    _sleep_seconds: int
    _queue_url: str
    _upload_bucket: str
    _crawler_proxies_manager = ProxiesManager()

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
                    # TODO: change back to logging.error
                    logging.warning(ex)
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

        if not self._should_crawl(url):
            return

        content, redirected_url = self._crawler_proxies_manager.crawl(url)

        self._process_response(url, redirected_url, content)

    def _delete_message(self, receipt_handle):
        SQS.delete_message(self._queue_url, receipt_handle)

    @staticmethod
    def _parse_message(message_body: str) -> (str, str):
        """
        Parse the message
        """
        body_obj = json.loads(message_body)
        if 'url' not in body_obj:
            raise MalFormedMessageException(f'Message {message_body} is malformed')

        return body_obj['url']

    def _should_crawl(self, url: str) -> bool:
        pass

    def _process_response(self, origin_url: str, final_url: str, content: str):
        pass
