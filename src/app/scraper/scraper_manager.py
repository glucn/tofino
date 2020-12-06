import threading

from app.scraper.linkedin_job_posting import LinkedInJobPostingScraper


class ScraperManager:
    """ Scraper manager """

    @classmethod
    def start(cls):
        scraper = LinkedInJobPostingScraper()

        t = threading.Thread(target=scraper.run, daemon=True)
        t.start()
