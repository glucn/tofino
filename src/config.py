# AWS
AWS_REGION = "us-west-2"

MYSQL_HOST = "tmwsfdnrcwbmp4.ca9x6xep5ulo.us-west-2.rds.amazonaws.com"
MYSQL_DB_NAME = "TOFINO_DB"
MYSQL_SECRET_NAME = "MySQL_application"

# LinkedIn
CRAWLER_LINKEDIN_JOB_POSTING_SQS_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/430714039810/tofino-LinkedInJobPostingCrawlerQueue-1UIGKFVGT2E4T'
SCRAPER_LINKEDIN_JOB_POSTING_SQS_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/430714039810/tofino-LinkedInJobPostingNotificationQueue-1TO6R1H3OI45S'
SCRAPER_LINKEDIN_JOB_SEARCH_RESULT_SQS_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/430714039810/tofino-LinkedInJobSearchResultNotificationQueue-GL08EWW9SMMA'
BUCKET_LINKEDIN_JOB_POSTING = 'tofino-linkedinjobpostingbucket-1w6vbf8dm64go'

# Indeed
CRAWLER_INDEED_JOB_POSTING_SQS_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/430714039810/tofino-IndeedJobPostingCrawlerQueue-USON2IW35VV8'
CRAWLER_INDEED_JOB_SEARCH_RESULT_SQS_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/430714039810/tofino-IndeedJobSearchResultCrawlerQueue-GH0NRC0D4XJO'
SCRAPER_INDEED_JOB_POSTING_SQS_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/430714039810/tofino-IndeedJobPostingNotificationQueue-E2ASFNKM95RK'
SCRAPER_INDEED_JOB_SEARCH_RESULT_SQS_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/430714039810/tofino-IndeedJobSearchResultNotificationQueue-1C072NHTD2010'
BUCKET_INDEED_JOB_POSTING = 'tofino-indeedjobpostingbucket-vwf5ud6vdepl'
BUCKET_INDEED_JOB_SEARCH_RESULT = 'tofino-indeedjobsearchresultbucket-qy5bbfkrksma'
