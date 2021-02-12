import logging
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

import config
from app.db_operator.mysql_client import MySQLClient
from app.exceptions import RetryableException
from app.models.job_posting import JobPosting
from app.scraper.base_scraper import BaseScraperWorker


def _parse_posted_datetime(soup: BeautifulSoup) -> datetime:
    if not soup.find("div", class_="jobsearch-JobMetadataFooter"):
        return datetime.now()

    footers = soup.find("div", class_="jobsearch-JobMetadataFooter").stripped_strings
    for s in footers:
        if s.endswith(" days ago"):
            if s.replace(" days ago", "") == "30+":
                n = 30
            else:
                n = int(s.replace(" days ago", ""))
            dt = datetime.now() - timedelta(days=n)
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if s == "1 day ago":
            dt = datetime.now() - timedelta(days=1)
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if s == "Today":
            dt = datetime.now()
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    return datetime.now()


class IndeedJobPostingScraper(BaseScraperWorker):
    """ Scrape Indeed's job posting page """

    def __init__(self):
        sleep_seconds = 30
        super().__init__('IndeedJobPostingScraper', config.SCRAPER_INDEED_JOB_POSTING_SQS_QUEUE_URL, sleep_seconds)

    def _scrape(self, file: str, file_name: str):
        if not file:
            # TODO: change back to logging.error
            logging.warning(f'[{self._worker_name}] Received an empty file [{file_name}]')
            return

        soup = BeautifulSoup(file, 'html.parser')

        title_h1 = soup.find("h1", class_="jobsearch-JobInfoHeader-title")
        if title_h1:
            job_title = title_h1.string
        else:
            job_title = ''

        jd_div = soup.find("div", class_="jobsearch-jobDescriptionText")
        if jd_div:
            job_description = '\n'.join([x for x in jd_div.strings])
        else:
            job_description = ''

        company_div = soup.find("div", class_="jobsearch-InlineCompanyRating")
        if company_div and company_div.contents:
            company_name = company_div.contents[0].string
        else:
            company_name = ''

        subtitle_div = soup.find("div", class_="jobsearch-JobInfoHeader-subtitle")
        if subtitle_div and subtitle_div.contents:
            location_string = subtitle_div.contents[-1].string
        else:
            location_string = ''

        posted_datetime = _parse_posted_datetime(soup)

        logging.info(f'[{self._worker_name}] Updating JobPosting record...')
        logging.info(f'[{self._worker_name}] Data: {job_title}, {company_name}, {location_string}')

        session = MySQLClient.get_session()
        try:
            job_posting = JobPosting.update(
                session=session,
                job_posting_id=file_name,
                title=job_title,
                company_name=company_name,
                location_string=location_string,
                job_description=job_description,
                posted_datetime=posted_datetime,
            )
            session.commit()
            logging.info(f'[{self._worker_name}] Updated JobPosting record {job_posting.id}')
        except Exception as ex:
            # TODO: change back to logging.error
            logging.warning(f'[{self._worker_name}] Error updating JobPosting record, rolling back...', ex)
            session.rollback()
            raise RetryableException
        except:
            # TODO: change back to logging.error
            logging.warning(f'[{self._worker_name}] Unexpected exception, rolling back...')
            session.rollback()
            raise RetryableException
        finally:
            session.close()
