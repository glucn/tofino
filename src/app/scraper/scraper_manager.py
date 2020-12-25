import threading

# from app.scraper.linkedin_job_posting import LinkedInJobPostingScraper
# from app.scraper.linkedin_job_search_result import LinkedInJobSearchResultScraper
from app.scraper.indeed_job_posting import IndeedJobPostingScraper
from app.scraper.indeed_job_search_result import IndeedJobSearchResultScraper


class ScraperManager:
    """ Scraper manager """

    @classmethod
    def start(cls):
        scrapers = [
            # LinkedInJobPostingScraper(),
            # LinkedInJobSearchResultScraper(),
            IndeedJobPostingScraper(),
            IndeedJobSearchResultScraper(),
        ]

        for scraper in scrapers:
            t = threading.Thread(target=scraper.run, daemon=True)
            t.start()
