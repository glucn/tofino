import threading

from app.scraper.linkedin_job_posting import LinkedInJobPostingScraper
from app.scraper.linkedin_job_search_result import LinkedInJobSearchResultScraper


class ScraperManager:
    """ Scraper manager """

    @classmethod
    def start(cls):
        scrapers = [
            # LinkedInJobPostingScraper(),
            # LinkedInJobSearchResultScraper(),
        ]

        for scraper in scrapers:
            t = threading.Thread(target=scraper.run, daemon=True)
            t.start()
