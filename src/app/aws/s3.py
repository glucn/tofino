import io

import boto3
from botocore.exceptions import ClientError

import config


class S3:
    """
    The client of AWS S3
    """
    _client = None

    @classmethod
    def _get_client(cls):
        if not cls._client:
            session = boto3.session.Session()
            cls._client = session.client(
                service_name='s3',
                region_name=config.AWS_REGION
            )
        return cls._client

    @classmethod
    def download_file_str(cls, bucket: str, key: str, encoding: str = 'utf-8') -> str:
        """
        Download an object from S3 to a string.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_fileobj

        :param bucket:
        :param key:
        :param encoding:
        :return:
        """
        if not bucket:
            raise ValueError(u'bucket is required')

        if not key:
            raise ValueError(u'key is required')

        try:
            bytes_buffer = io.BytesIO()

            cls._get_client().download_fileobj(
                Bucket=bucket,
                Key=key,
                Fileobj=bytes_buffer
            )

            byte_value = bytes_buffer.getvalue()
            return byte_value.decode(encoding)

        except ClientError as e:
            raise e

    @classmethod
    def put_object(cls, bucket: str, key: str, body: object) -> None:
        """
        Adds an object to a bucket. TODO: implement me

        :param bucket:
        :param key:
        :param body:
        :return:
        """
        pass
