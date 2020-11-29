import hashlib
from typing import List

import boto3
from botocore.exceptions import ClientError

import config


class Message:
    """
    SQS Message
    """
    message_id: str
    receipt_handle: str
    body: str

    _representation: str

    def __init__(self, **kwargs):
        if 'ReceiptHandle' in kwargs:
            self.receipt_handle = kwargs['ReceiptHandle']
        else:
            raise ValueError('ReceiptHandle is required')

        self.message_id = kwargs['MessageId'] if 'MessageId' in kwargs else None

        if 'Body' in kwargs:
            if 'MD5OfBody' in kwargs:
                body_hash = hashlib.md5(kwargs['Body'].encode('utf-8')).hexdigest()
                if body_hash != kwargs['MD5OfBody']:
                    raise ValueError(
                        u'MD5 hash of Body %s does not match MD5OfBody %s' % (kwargs['Body'], kwargs['MD5OfBody']))
            self.body = kwargs['Body']

        self._representation = u'Message(message_id: {0}, receipt_handle: {1}, body: {2})'.format(
            self.message_id, self.receipt_handle, self.body)

    def __repr__(self):
        return self._representation

    def __str__(self):
        return self._representation


class SQS:
    """
    The client of AWS SQS
    """
    _client = None

    @classmethod
    def _get_client(cls):
        if not cls._client:
            session = boto3.session.Session()
            cls._client = session.client(
                service_name='sqs',
                region_name=config.AWS_REGION
            )
        return cls._client

    @classmethod
    def receive_message(cls,
                        queue_url: str,
                        max_number_of_messages: int = 1,
                        wait_time_seconds: int = 1) -> List[Message]:
        """
        Retrieves one or more messages (up to 10), from the specified queue.
        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html

        :param queue_url: The URL of the Amazon SQS queue from which messages are received (case-sensitive).
        :param max_number_of_messages: The maximum number of messages to return. Valid values: 1 to 10. Default: 1.
        :param wait_time_seconds: The duration (in seconds) for which the call waits for a message to arrive in
                                  the queue before returning. Default: 1.
        :return: A list of messages
        """
        if not queue_url:
            raise ValueError(u'queue_url is required')

        if max_number_of_messages < 1 or max_number_of_messages > 10:
            raise ValueError(u'max_number_of_messages valid values: 1 to 10')

        try:
            receive_message_response = cls._get_client().receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_number_of_messages,
                WaitTimeSeconds=wait_time_seconds,
            )

            if 'Messages' in receive_message_response:
                return [Message(**message) for message in receive_message_response['Messages']]
            else:
                return []

        except ClientError as e:
            raise e

    @classmethod
    def delete_message(cls, queue_url: str, receipt_handle: str) -> None:
        """
        Deletes the specified message from the specified queue.
        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteMessage.html

        :param queue_url: The URL of the Amazon SQS queue from which messages are deleted.
        :param receipt_handle: The receipt handle associated with the message to delete.
        :return: None
        """
        if not queue_url:
            raise ValueError(u'queue_url is required')

        if not receipt_handle:
            raise ValueError(u'receipt_handle is required')

        try:
            cls._get_client().delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle,
            )

        except ClientError as e:
            raise e
