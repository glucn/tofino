import io
import logging

import boto3
import urllib3
from botocore.exceptions import ClientError


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
                region_name='us-west-2'
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
            logging.error(e)
            raise e

    @classmethod
    def upload_file_obj(cls, file: object, bucket: str, key: str) -> None:
        """
        Upload a file-like object to S3.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_fileobj

        :param file:
        :param bucket:
        :param key:
        :return:
        """
        if not file:
            raise ValueError(u'file is require')

        if not bucket:
            raise ValueError(u'bucket is required')

        if not key:
            raise ValueError(u'key is required')

        try:
            cls._get_client().upload_fileobj(file, bucket, key)

        except ClientError as e:
            logging.error(e)
            raise e


def crawl(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'text/html',
    }

    http = urllib3.PoolManager()
    response = http.request('GET', url, headers=headers)

    return response.geturl(), response.data


if __name__ == '__main__':
    url = 'https://ca.indeed.com/job/data-entry-analyst-dd4e1204edf15b10'
    id = '40694490-db56-4915-a60b-c09c9ffc7357'

    _, content = crawl(url)

    S3.upload_file_obj(io.BytesIO(content), 'tofino-indeedjobpostingbucket-vwf5ud6vdepl', id)
