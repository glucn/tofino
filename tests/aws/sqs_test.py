from unittest import TestCase
from unittest.mock import patch, MagicMock

from app.aws import SQS
from app.aws.sqs import Message


class MessageTest(TestCase):
    def test_constructor_should_raise_value_error_when_receipt_handle_is_empty(self):
        with self.assertRaises(ValueError):
            Message(**{'MessageId': 'id-1'})

    def test_constructor_should_raise_value_error_when_md5_does_not_match_the_body(self):
        with self.assertRaises(ValueError):
            Message(**{
                'MessageId': 'id-1',
                'ReceiptHandle': 'handle-1',
                'Body': '{"test":"abc"}',
                'MD5OfBody': 'wrong-md5',
            })

    def test_constructor_happy_path(self):
        message = Message(**{
                'MessageId': 'id-1',
                'ReceiptHandle': 'handle-1',
                'Body': '{"test":"abc"}',
                'MD5OfBody': '7f2d037ef02d2b24b045fb6492def5bd',
            })
        self.assertEqual(message.message_id, 'id-1')
        self.assertEqual(message.receipt_handle, 'handle-1')
        self.assertEqual(message.body, '{"test":"abc"}')


class SQSTest(TestCase):
    test_queue_url = 'https://sqs.amazonaws.com/123456789123/test-queue'

    mock_client = MagicMock()

    def test_receive_message_should_raise_value_error_when_queue_url_is_empty(self):
        with self.assertRaises(ValueError):
            SQS.receive_message('')

    def test_receive_message_should_raise_value_error_when_max_number_of_messages_is_less_than_1(self):
        with self.assertRaises(ValueError):
            SQS.receive_message(self.test_queue_url, 0)

    def test_receive_message_should_raise_value_error_when_max_number_of_messages_is_greater_than_10(self):
        with self.assertRaises(ValueError):
            SQS.receive_message(self.test_queue_url, 11)

    @patch('app.aws.sqs.SQS._get_client', mock_client)
    def test_receive_message_should_return_empty_list_when_no_message_is_returned(self):
        self.mock_client.return_value.receive_message.return_value = {
            'ResponseMetadata': {},
            'RetryAttempts': 0,
        }
        result = SQS.receive_message(self.test_queue_url)
        self.assertEqual(result, [])

    @patch('app.aws.sqs.SQS._get_client', mock_client)
    def test_receive_message_should_return_a_list_of_messages(self):
        self.mock_client.return_value.receive_message.return_value = {
            'Messages': [
                {
                    'MessageId': 'id-1',
                    'ReceiptHandle': 'handle-1',
                    'Body': '{}'
                },
                {
                    'MessageId': 'id-2',
                    'ReceiptHandle': 'handle-2',
                    'Body': '{}'
                }
            ],
            'ResponseMetadata': {},
            'RetryAttempts': 0,
        }
        result = SQS.receive_message(self.test_queue_url)
        # TODO: assert the result contains two expected Message objects
        self.assertEqual(len(result), 2)

