import logging
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

import config
from app.db_operator.mysql_client import MySQLClient
from app.exceptions import RetryableException
from app.models.job_posting import JobPosting
from app.scraper.base_scraper import BaseScraperWorker


def _parse_posted_datetime(soup: BeautifulSoup) -> datetime:
    footers = soup.find("div", class_="jobsearch-JobMetadataFooter").stripped_strings
    for s in footers:
        if s.endswith(" days ago"):
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
        soup = BeautifulSoup(file, 'html.parser')

        job_title = soup.find("h1", class_="jobsearch-JobInfoHeader-title").string
        job_description = '\n'.join([x for x in soup.find("div", class_="jobsearch-jobDescriptionText").strings])
        company_name = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[0].string
        location_string = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[-1].string
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
            logging.error(f'[{self._worker_name}] Error updating JobPosting record, rolling back...', ex)
            session.rollback()
            raise RetryableException
        except:
            logging.error(f'[{self._worker_name}] Unexpected exception, rolling back...')
            session.rollback()
            raise RetryableException
        finally:
            session.close()
