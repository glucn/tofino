import json
import logging
import random
from datetime import datetime, timedelta

from typing import List, Optional

from app.aws import Lambda
from app.exceptions import RetryableException
from config import crawlers


class Proxy:
    region: str
    arn: str
    deactivated: Optional[datetime]

    DEACTIVATED_WAIT_TIME = timedelta(hours=12)

    def __init__(self, region, arn):
        self.region = region
        self.arn = arn
        self.deactivated = None

    def is_active(self):
        now = datetime.now()
        return self.deactivated is None or now > self.deactivated + self.DEACTIVATED_WAIT_TIME

    def deactivate(self):
        self.deactivated = datetime.now()


class ProxiesManager:
    """ The manager for proxy Lambda functions """

    _proxies: List[Proxy]

    def __init__(self):
        self._proxies = [Proxy(c['region'], c['arn']) for c in crawlers]

    def _get_random_proxy(self):
        available_proxies = [p for p in self._proxies if p.is_active()]
        return available_proxies[random.randrange(len(available_proxies))]

    def crawl(self, url: str) -> (str, str):
        crawler_proxy = self._get_random_proxy()
        r = Lambda.invoke(crawler_proxy.region, crawler_proxy.arn, json.dumps({'url': url}))
        response = json.loads(r)
        if response['statusCode'] != 200:
            # TODO: change back to logging.error
            logging.warning(f'Getting URL "{url}" resulted in status code {response["statusCode"]}')
            crawler_proxy.deactivate()
            raise RetryableException

        if not response["content"]:
            logging.warning(f'Proxy in region [{crawler_proxy.region}] received empty content')
            crawler_proxy.deactivate()
            raise RetryableException

        return response["content"], response["url"]
