import config
from app.crawler.base_crawler import BaseCrawlerWorker


class IndeedJobPostingCrawler(BaseCrawlerWorker):
    """ Crawl Indeed's job posting page """

    def __init__(self):
        super().__init__('IndeedJobPostingCrawler',
                         config.CRAWLER_INDEED_JOB_POSTING_SQS_QUEUE_URL,
                         config.BUCKET_INDEED_JOB_POSTING,
                         60)
