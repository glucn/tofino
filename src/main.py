import os
from logging.config import fileConfig
from os import path

from flask import Flask, request
from flask_cors import CORS

from app.crawler import CrawlerManager
from app.handlers.job_posting import JobPostingHandler
from app.handlers.resume_assitant import ResumeAssistantHandler
from app.scraper import ScraperManager

if not os.path.exists("logs/"):
    os.makedirs("logs/")

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.cfg')
fileConfig(log_file_path)


@app.route('/healthz', methods=['GET'])
def shallow_healthy_check():
    return '{}', 200, {'Content-Type': 'application/json'}


@app.route('/api/v1/jobPosting/<job_posting_id>', methods=['GET'])
def get(job_posting_id):
    return JobPostingHandler.get(job_posting_id)


@app.route('/api/v1/jobPosting', methods=['POST'])
@app.route('/api/v1/jobPosting/', methods=['POST'])
def create():
    return JobPostingHandler.create(**request.get_json())


@app.route('/api/v1/jobPosting/<job_posting_id>', methods=['POST'])
def update(job_posting_id):
    return JobPostingHandler.update(job_posting_id, **request.get_json())


@app.route('/api/v1/jobPosting/<job_posting_id>', methods=['DELETE'])
def delete(job_posting_id):
    return JobPostingHandler.delete(job_posting_id)


@app.route('/api/v1/resume/analyze', methods=['POST'])
def analyze_resume():
    return ResumeAssistantHandler.analyze(**request.get_json())


if __name__ == '__main__':
    ScraperManager.start()
    CrawlerManager.start()
    app.run(host="0.0.0.0")
