import threading

# from app.crawler.linkedin_job_posting import LinkedInJobPostingCrawler
from app.crawler.indeed_job_posting import IndeedJobPostingCrawler
from app.crawler.indeed_job_search_result import IndeedJobSearchResultCrawler


class CrawlerManager:
    """ Crawler manager """

    @classmethod
    def start(cls):
        crawlers = [
            # LinkedInJobPostingCrawler(),
            # IndeedJobPostingCrawler(),
            IndeedJobSearchResultCrawler(),
        ]

        for crawlers in crawlers:
            t = threading.Thread(target=crawlers.run, daemon=True)
            t.start()
