""" API handlers of JobPosting """
import dataclasses
import json

import flask

from app.db_operator.mysql_client import MySQLClient
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

        session = MySQLClient.get_session()
        try:
            job_posting = JobPosting.get(session, job_posting_id)
            if not job_posting:
                flask.abort(404, f"job posting with id {job_posting_id} cannot be found")

            return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER
        finally:
            session.close()

    @classmethod
    def create(cls, **kwargs):
        session = MySQLClient.get_session()
        try:
            job_posting = JobPosting.create(session, **kwargs)
            if not job_posting:
                flask.abort(500, "Internal Failure")
            session.commit()

            return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER
        finally:
            session.close()

    @classmethod
    def update(cls, job_posting_id, **kwargs):
        if not job_posting_id:
            flask.abort(400, "job_posting_id is required")

        session = MySQLClient.get_session()
        try:
            job_posting = JobPosting.update(session, job_posting_id, **kwargs)
            if not job_posting:
                flask.abort(500, "Internal Failure")

            session.commit()

            return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER
        finally:
            session.close()

    @classmethod
    def delete(cls, job_posting_id):
        if not job_posting_id:
            flask.abort(400, "job_posting_id is required")
        session = MySQLClient.get_session()
        try:
            job_posting = JobPosting.delete(session, job_posting_id)
            if not job_posting:
                flask.abort(500, "Internal Failure")

            session.commit()

            return json.dumps(dataclasses.asdict(job_posting), default=json_serialize), 200, cls.JSON_HEADER
        finally:
            session.close()
