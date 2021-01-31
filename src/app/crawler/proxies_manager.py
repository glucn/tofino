import json
import logging
import random
from datetime import datetime, timedelta

from app.aws import Lambda
from app.db_operator.mysql_client import MySQLClient
from app.exceptions import RetryableException
from app.models.crawler_proxy import CrawlerProxy

DEACTIVATED_WAIT_TIME = timedelta(hours=12)


class ProxiesManager:
    """ The manager for proxy Lambda functions """

    @staticmethod
    def _get_random_proxy() -> CrawlerProxy:
        session = MySQLClient.get_session()
        try:
            available_proxies = CrawlerProxy.list_active(session, datetime.now() - DEACTIVATED_WAIT_TIME)
            if len(available_proxies) == 0:
                logging.warning(f'There is no active proxy at the moment')
                raise RetryableException
            return available_proxies[random.randrange(len(available_proxies))]
        finally:
            session.close()

    @staticmethod
    def _deactivate_proxy(proxy_id: str):
        session = MySQLClient.get_session()
        try:
            proxy = CrawlerProxy.get(session, proxy_id)
            CrawlerProxy.update(
                session=session,
                proxy_id=proxy_id,
                deactivated_datetime=datetime.now(),
                deactivated_count=proxy.deactivated_count + 1,
            )
            session.commit()
        except Exception as ex:
            session.rollback()
            raise RetryableException(ex)
        finally:
            session.close()

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
            self._deactivate_proxy(crawler_proxy.id)
            raise RetryableException

        if 'www.hcaptcha.com' in response["content"]:
            logging.warning(f'Proxy in region [{crawler_proxy.region}] received hcaptcha check')
            crawler_proxy.deactivate()
            raise RetryableException

        return response["content"], response["url"]
