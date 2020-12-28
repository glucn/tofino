import logging

from bs4 import BeautifulSoup

import config
from app.db_operator.mysql_client import MySQLClient
from app.exceptions import RetryableException
from app.models.job_posting import JobPosting
from app.scraper.base_scraper import BaseScraperWorker


class IndeedJobPostingScraper(BaseScraperWorker):
    """ Scrape Indeed's job posting page """

    _SOURCE = 'ca.indeed.com'
    _URL = 'https://ca.indeed.com'  # URL cannot be null in DB schema TODO: retrieve the real URL instead of this

    def __init__(self):
        super().__init__('IndeedJobPostingScraper', config.SCRAPER_INDEED_JOB_POSTING_SQS_QUEUE_URL)

    def _scrape(self, file: str):
        logging.info('IndeedJobPostingScraper is scraping')

        soup = BeautifulSoup(file, 'html.parser')

        job_title = soup.find("h1", class_="jobsearch-JobInfoHeader-title").string
        job_description = '\n'.join([x for x in soup.find("div", class_="jobsearch-jobDescriptionText").strings])
        company_name = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[0].string
        location_string = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[3].string

        logging.info(f'[{self._worker_name}] Creating JobPosting record...')
        logging.info(f'[{self._worker_name}] Data: {job_title}, {company_name}, {location_string}')

        session = MySQLClient.get_session()
        try:
            job_posting = JobPosting.create(
                session=session,
                source=self._SOURCE,
                url=self._URL,
                title=job_title,
                company_name=company_name,
                location_string=location_string,
                job_description=job_description,
            )
            logging.info(f'[{self._worker_name}] Committing...')
            session.commit()
            logging.info(f'[{self._worker_name}] Created JobPosting record {job_posting.id}')
        except Exception as ex:
            logging.error(f'[{self._worker_name}] Error creating JobPosting record, rolling back...', ex)
            session.rollback()
            raise RetryableException
        except:
            logging.error(f'[{self._worker_name}] Unexpected exception, rolling back...')
            session.rollback()
            raise RetryableException
        finally:
            logging.info(f'[{self._worker_name}] Closing session...')
            session.close()
