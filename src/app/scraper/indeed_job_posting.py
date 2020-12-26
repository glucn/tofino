import logging

from bs4 import BeautifulSoup

import config
from app.models.job_posting import JobPosting
from app.scraper.base_scraper import BaseScraperWorker


class IndeedJobPostingScraper(BaseScraperWorker):
    """ Scrape Indeed's job posting page """

    _SOURCE = 'ca.indeed.com'

    def __init__(self):
        super().__init__('IndeedJobPostingScraper', config.SCRAPER_INDEED_JOB_POSTING_SQS_QUEUE_URL)

    def _scrape(self, file: str):
        logging.info('IndeedJobPostingScraper is scraping')

        soup = BeautifulSoup(file, 'html.parser')

        job_title = soup.find("h1", class_="jobsearch-JobInfoHeader-title").string
        job_description = '\n'.join([x for x in soup.find("div", class_="jobsearch-jobDescriptionText").strings])
        company_name = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[0].string
        location_string = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[3].string

        job_posting = JobPosting.create(
            source=self._SOURCE,
            title=job_title,
            company_name=company_name,
            location_string=location_string,
            job_description=job_description,
        )
        logging.info(f'[{self._worker_name}] Created JobPosting record {job_posting.id}')

