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
