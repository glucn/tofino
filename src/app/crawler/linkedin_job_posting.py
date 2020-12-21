import config
from app.crawler.base_crawler import BaseCrawlerWorker


class LinkedInJobPostingCrawler(BaseCrawlerWorker):
    """ Crawl LinkedIn's job posting page """

    def __init__(self):
        super().__init__('LinkedInJobPostingCrawler',
                         config.CRAWLER_LINKEDIN_JOB_POSTING_SQS_QUEUE_URL,
                         config.BUCKET_LINKEDIN_JOB_POSTING,
                         10)
