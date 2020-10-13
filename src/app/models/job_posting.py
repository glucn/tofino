import uuid

from app.db_operator import db


class JobPosting(db.Model):
    """ Data model of Job Postings """

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
    def create(cls, url, **kwargs):
        job_posting_id = uuid.uuid4()
        job_posting = cls(id=job_posting_id, url=url, **kwargs)
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
