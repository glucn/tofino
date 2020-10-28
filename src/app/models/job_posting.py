import uuid
from dataclasses import dataclass
from datetime import datetime

from app.db_operator import db


@dataclass
class JobPosting(db.Model):
    """ Data model of Job Postings """
    id: str
    url: str
    source: str
    title: str
    company_id: str
    company_name: str
    location_string: str
    posted_datetime: datetime
    job_description: str

    __tablename__ = "testing"

    id = db.Column(db.String(50), primary_key=True)
    url = db.Column(db.String(256))
    source = db.Column(db.String(256))
    title = db.Column(db.String(256))
    company_id = db.Column(db.String(50))
    company_name = db.Column(db.String(256))
    location_string = db.Column(db.String(256))
    posted_datetime = db.Column(db.DateTime)
    job_description = db.Column(db.String(10000))

    @classmethod
    def get(cls, job_posting_id):
        return cls.query.get(job_posting_id)

    @classmethod
    def create(cls, **kwargs):
        job_posting_id = uuid.uuid4()
        job_posting = cls(id=str(job_posting_id), **kwargs)
        db.session.add(job_posting)
        db.session.commit()
        return job_posting

    @classmethod
    def update(cls, job_posting_id, **kwargs):
        job_posting = db.session.query(cls).get(job_posting_id)

        if not job_posting:
            raise ValueError(u'job posting with id %s does not exist', job_posting_id)

        for k, v in kwargs.items():
            setattr(job_posting, k, v)

        db.session.commit()
        return job_posting

    @classmethod
    def delete(cls, job_posting_id):
        job_posting = db.session.query(cls).get(job_posting_id)

        if not job_posting:
            raise ValueError(u'job posting with id %s does not exist', job_posting_id)

        db.session.delete(job_posting)
        db.session.commit()
        return job_posting
