import logging
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class JobPosting(Base):
    """ Data model of Job Postings """
    id: str
    external_id: str
    url: str
    origin_url: str
    source: str
    title: str
    company_id: str
    company_name: str
    location_string: str
    posted_datetime: datetime
    job_description: str
    created_datetime: datetime
    updated_datetime: datetime

    __tablename__ = "job_posting"

    id = Column(String(256), primary_key=True)
    external_id = Column(String(256))
    url = Column(String(256))
    origin_url = Column(String(2048))
    source = Column(String(256))
    title = Column(String(256))
    company_id = Column(String(50))
    company_name = Column(String(256))
    location_string = Column(String(256))
    posted_datetime = Column(DateTime)
    job_description = Column(String(10000))
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, str):
                try:
                    self.__setattr__(k, datetime.strptime(v, "%Y-%m-%dT%H:%M:%S%z"))
                except ValueError:  # This exception is expected if the string is not a ISO8601 datetime
                    self.__setattr__(k, v)
            else:
                self.__setattr__(k, v)

    @classmethod
    def get(cls, session, job_posting_id):
        return session.query(cls).filter(cls.id == job_posting_id).one_or_none()

    @classmethod
    def get_by_external_id(cls, session, source, external_id):
        return session.query(cls).filter(cls.source == source, cls.external_id == external_id).one_or_none()

    @classmethod
    def get_by_url(cls, session, url):
        return session.query(cls).filter(cls.url == url).one_or_none()

    @classmethod
    def get_by_origin_url(cls, session, origin_url):
        return session.query(cls).filter(cls.origin_url == origin_url).one_or_none()

    @classmethod
    def create(cls, session, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())

        job_posting = cls(**kwargs)
        job_posting.created_datetime = datetime.now()

        session.add(job_posting)
        return job_posting

    @classmethod
    def update(cls, session, job_posting_id, **kwargs):
        logging.debug(f'update is called with {job_posting_id}, {kwargs}')
        job_posting = session.query(cls).filter(cls.id == job_posting_id).one()

        if not job_posting:
            raise ValueError(u'job posting with id %s does not exist', job_posting_id)

        for k, v in kwargs.items():
            if type(v) == str:
                setattr(job_posting, k, cls._cleansing_string(v))
            else:
                setattr(job_posting, k, v)

        job_posting.updated_datetime = datetime.now()
        session.add(job_posting)
        return job_posting

    @classmethod
    def delete(cls, session, job_posting_id):
        job_posting = session.query(cls).filter(cls.id == job_posting_id).one()

        if not job_posting:
            raise ValueError(u'job posting with id %s does not exist', job_posting_id)

        session.delete(job_posting)
        return job_posting

    @classmethod
    def _cleansing_string(cls, content: str) -> str:
        return content.replace(u'\ufeff', '')
