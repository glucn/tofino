import threading

# from app.crawler.linkedin_job_posting import LinkedInJobPostingCrawler


class CrawlerManager:
    """ Crawler manager """

    @classmethod
    def start(cls):
        crawlers = [
            # LinkedInJobPostingCrawler(),
        ]

        for crawlers in crawlers:
            t = threading.Thread(target=crawlers.run, daemon=True)
            t.start()
