from flask import Flask

from app.db_operator.mysql_client import MySQLClient, db
from app.handlers.job_posting import JobPostingHandler

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = MySQLClient.get_sqlalchemy_connection_string()
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_ECHO'] = True

db.init_app(APP)


@APP.route('/api/v1/jobPosting/<job_posting_id>')
def get(job_posting_id):
    return JobPostingHandler.get(job_posting_id)
