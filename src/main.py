import os
from logging.config import fileConfig

from flask import Flask, request

from app.db_operator.mysql_client import MySQLClient, db
from app.handlers.job_posting import JobPostingHandler
from app.scraper import ScraperManager

if not os.path.exists("logs/"):
    os.makedirs("logs/")

APP = Flask(__name__)
fileConfig('logging.cfg')

APP.config['SQLALCHEMY_DATABASE_URI'] = MySQLClient.get_sqlalchemy_connection_string()
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_ECHO'] = True

db.init_app(APP)


@APP.route('/healthz', methods=['GET'])
def shallow_healthy_check():
    return '{}', 200, {'Content-Type': 'application/json'}


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


if __name__ == '__main__':
    ScraperManager.start()
    APP.run(host="0.0.0.0")
