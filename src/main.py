from flask import Flask

from app.db_operator.mysql_client import MySQLClient, db
from app.models.job_posting import JobPosting

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = MySQLClient.get_sqlalchemy_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

# TODO: kill these prototype code
app.app_context().push()
# print(JobPosting.query.all())
# jp = JobPosting.get("123")
# print(jp.url)

# from datetime import datetime
# jp = JobPosting.create(url="http://test.com", title="test create", posted_datetime=datetime.now())
# jp = JobPosting.update(job_posting_id="123", posted_datetime=datetime.now())
# jp = JobPosting.delete(job_posting_id="a1822c03-a321-4f50-910b-5d570c694a98")
