from flask import Flask, request

from app.db_operator.mysql_client import MySQLClient, db
from app.handlers.job_posting import JobPostingHandler

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = MySQLClient.get_sqlalchemy_connection_string()
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_ECHO'] = True

db.init_app(APP)


@APP.route('/healthz', method=['GET'])
def shallow_healthy_check():
    return '{}'


@APP.route('/api/v1/jobPosting/<job_posting_id>', methods=['GET'])
def get(job_posting_id):
    return JobPostingHandler.get(job_posting_id)


@APP.route('/api/v1/jobPosting', methods=['POST'])
@APP.route('/api/v1/jobPosting/', methods=['POST'])
def create():
    return JobPostingHandler.create(**request.get_json())


@APP.route('/api/v1/jobPosting/<job_posting_id>', methods=['POST'])
def update(job_posting_id):
    return JobPostingHandler.update(job_posting_id, **request.get_json())


@APP.route('/api/v1/jobPosting/<job_posting_id>', methods=['DELETE'])
def delete(job_posting_id):
    return JobPostingHandler.delete(job_posting_id)
