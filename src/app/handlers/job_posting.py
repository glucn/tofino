""" API handlers of JobPosting """
import dataclasses
import json

import flask

from app.handlers.base_handler import BaseHandler

from app.models.job_posting import JobPosting
from app.utils import json_serialize


class JobPostingHandler(BaseHandler):
    """
    API handler for JobPosting
    """

    JSON_HEADER = {'Content-Type': 'application/json'}

    @classmethod
    def get(cls, job_posting_id):
        if not job_posting_id:
            flask.abort(400, "job_posting_id is required")

        job_posting = JobPosting.get(job_posting_id)
        if not job_posting:
            flask.abort(404, f"job posting with id {job_posting_id} cannot be found")

        return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER

    @classmethod
    def create(cls, **kwargs):
        job_posting = JobPosting.create(**kwargs)

        if not job_posting:
            flask.abort(500, "Internal Failure")

        return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER

    @classmethod
    def update(cls, job_posting_id, **kwargs):
        if not job_posting_id:
            flask.abort(400, "job_posting_id is required")

        job_posting = JobPosting.update(job_posting_id, **kwargs)

        if not job_posting:
            flask.abort(500, "Internal Failure")

        return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER

    @classmethod
    def delete(cls, job_posting_id):
        if not job_posting_id:
            flask.abort(400, "job_posting_id is required")

        job_posting = JobPosting.delete(job_posting_id)
        if not job_posting:
            flask.abort(500, "Internal Failure")

        return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER
