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
        self.assertEqual(ex.exception.code, 400)

    @patch('app.models.job_posting.JobPosting.get')
    def test_get_should_throw_404_error_if_job_posting_does_not_exist(self, mock_get):
        mock_get.return_value = None
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.get(self.test_job_posting.id)
        self.assertEqual(ex.exception.code, 404)
        mock_get.assert_called_once_with(self.test_job_posting.id)

    @patch('app.models.job_posting.JobPosting.get')
    def test_get_should_return_json_string_of_job_posting(self, mock_get):
        mock_get.return_value = self.test_job_posting
        result, code, header = JobPostingHandler.get(self.test_job_posting.id)
        self.assertEqual(self.test_job_posting, json.loads(result, object_hook=lambda d: JobPosting(**d)))
        mock_get.assert_called_once_with(self.test_job_posting.id)
        self.assertEqual(200, code)
        self.assertEqual({'Content-Type': 'application/json'}, header)

    @patch('app.models.job_posting.JobPosting.create')
    def test_create_should_throw_500_error_if_creating_fails(self, mock_create):
        mock_create.return_value = None
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.create(id=self.test_job_posting.id)
        self.assertEqual(ex.exception.code, 500)
        mock_create.assert_called_once_with(id=self.test_job_posting.id)

    @patch('app.models.job_posting.JobPosting.create')
    def test_create_should_return_json_string_of_job_posting(self, mock_create):
        mock_create.return_value = self.test_job_posting
        result, code, header = JobPostingHandler.create(**self.test_job_posting.__dict__)
        self.assertEqual(self.test_job_posting, json.loads(result, object_hook=lambda d: JobPosting(**d)))
        mock_create.assert_called_once_with(**self.test_job_posting.__dict__)
        self.assertEqual(200, code)
        self.assertEqual({'Content-Type': 'application/json'}, header)

    def test_update_should_throw_400_error_if_job_posting_id_is_null(self):
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.update(None)
        self.assertEqual(ex.exception.code, 400)

    @patch('app.models.job_posting.JobPosting.update')
    def test_update_should_throw_500_error_if_updating_fails(self, mock_update):
        mock_update.return_value = None
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.update(self.test_job_posting.id, **self.test_job_posting.__dict__)
        self.assertEqual(ex.exception.code, 500)
        mock_update.assert_called_once_with(self.test_job_posting.id, **self.test_job_posting.__dict__)

    @patch('app.models.job_posting.JobPosting.update')
    def test_update_should_return_json_string_of_job_posting(self, mock_update):
        mock_update.return_value = self.test_job_posting
        result, code, header = JobPostingHandler.update(self.test_job_posting.id, **self.test_job_posting.__dict__)
        self.assertEqual(self.test_job_posting, json.loads(result, object_hook=lambda d: JobPosting(**d)))
        mock_update.assert_called_once_with(self.test_job_posting.id, **self.test_job_posting.__dict__)
        self.assertEqual(200, code)
        self.assertEqual({'Content-Type': 'application/json'}, header)

    def test_delete_should_throw_400_error_if_job_posting_id_is_null(self):
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.delete(None)
        self.assertEqual(ex.exception.code, 400)

    @patch('app.models.job_posting.JobPosting.delete')
    def test_delete_should_throw_500_error_if_deleting_fails(self, mock_delete):
        mock_delete.return_value = None
        with self.assertRaises(HTTPException) as ex:
            JobPostingHandler.delete(self.test_job_posting.id)
        self.assertEqual(ex.exception.code, 500)
        mock_delete.assert_called_once_with(self.test_job_posting.id)

    @patch('app.models.job_posting.JobPosting.delete')
    def test_delete_should_return_json_string_of_job_posting(self, mock_delete):
        mock_delete.return_value = self.test_job_posting
        result, code, header = JobPostingHandler.delete(self.test_job_posting.id)
        self.assertEqual(self.test_job_posting, json.loads(result, object_hook=lambda d: JobPosting(**d)))
        mock_delete.assert_called_once_with(self.test_job_posting.id)
        self.assertEqual(200, code)
        self.assertEqual({'Content-Type': 'application/json'}, header)
