import json
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from dateutil import tz
from werkzeug.exceptions import HTTPException

from app.handlers.job_posting import JobPostingHandler
from app.models.job_posting import JobPosting


class JobPostingHandlerTest(TestCase):
    test_job_posting = JobPosting(
        id="id-123",
        url="http://example.com",
        source="Test Source",
        title="Test Title",
        company_id="comp-1234",
        company_name="Test Company",
        location_string="Test Location",
        posted_datetime=datetime(2020, 1, 1, 0, 0, 0, 0, tz.UTC),
        job_description="Test Description"
    )

    def test_get_should_throw_400_error_if_job_posting_id_is_null(self):
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.get(None)
        self.assertEqual(400, ex.exception.code)

    @patch('app.models.job_posting.JobPosting.get')
    def test_get_should_throw_404_error_if_job_posting_does_not_exist(self, mock_get):
        mock_get.return_value = None
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.get(self.test_job_posting.id)
        self.assertEqual(404, ex.exception.code)
        mock_get.assert_called_once_with(self.test_job_posting.id)

    @patch('app.models.job_posting.JobPosting.get')
    def test_get_should_return_json_string_of_job_posting(self, mock_get):
        mock_get.return_value = self.test_job_posting
        result = JobPostingHandler.get(self.test_job_posting.id)
        # TODO: figure out how to deserialize datetime
        # self.assertEqual(json.loads(result, object_hook=lambda d: JobPosting(**d)), self.test_job_posting)
        mock_get.assert_called_once_with(self.test_job_posting.id)

