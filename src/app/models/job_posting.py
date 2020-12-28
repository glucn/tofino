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
    source: str
    title: str
    company_id: str
    company_name: str
    location_string: str
    posted_datetime: datetime
    job_description: str

    __tablename__ = "testing"

    id = Column(String(256), primary_key=True)
    external_id = Column(String(256))
    url = Column(String(256))
    source = Column(String(256))
    title = Column(String(256))
    company_id = Column(String(50))
    company_name = Column(String(256))
    location_string = Column(String(256))
    posted_datetime = Column(DateTime)
    job_description = Column(String(10000))

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
        return session.query(cls).filter(cls.id == job_posting_id).one()

    @classmethod
    def create(cls, session, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())

        job_posting = cls(**kwargs)
        session.add(job_posting)
        return job_posting

    @classmethod
    def update(cls, session, job_posting_id, **kwargs):
        job_posting = session.query(cls).filter(cls.id == job_posting_id).one()

        if not job_posting:
            raise ValueError(u'job posting with id %s does not exist', job_posting_id)

        for k, v in kwargs.items():
            setattr(job_posting, k, v)

        session.add(job_posting)
        return job_posting

    @classmethod
    def delete(cls, session, job_posting_id):
        job_posting = session.query(cls).filter(cls.id == job_posting_id).one()

        if not job_posting:
            raise ValueError(u'job posting with id %s does not exist', job_posting_id)

        session.delete(job_posting)
        return job_posting
