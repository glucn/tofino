import threading

# from app.crawler.linkedin_job_posting import LinkedInJobPostingCrawler
from app.crawler.indeed_job_posting import IndeedJobPostingCrawler


class CrawlerManager:
    """ Crawler manager """

    @classmethod
    def start(cls):
        crawlers = [
            # LinkedInJobPostingCrawler(),
            IndeedJobPostingCrawler(),
        ]

        for crawlers in crawlers:
            t = threading.Thread(target=crawlers.run, daemon=True)
            t.start()
