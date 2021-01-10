import logging

import boto3
from botocore.exceptions import ClientError


class Lambda:
    """
    The client of AWS Lambda
    """
    _client = {}

    @classmethod
    def _get_client(cls, region: str):
        if not cls._client[region]:
            session = boto3.session.Session()
            cls._client[region] = session.client(
                service_name='lambda',
                region_name=region
            )
        return cls._client[region]

    @classmethod
    def invoke(cls, region: str, arn: str, payload: str) -> str:
        """
        Invokes a Lambda function

        :return:
        """
        if not region:
            raise ValueError(u'region is required')

        if not arn:
            raise ValueError(u'arn is required')

        logging.info(f'Invoke is called with region [{region}], arn [{arn}], payload {payload}')
        try:
            response = cls._get_client(region).invoke(
                FunctionName=arn,
                InvocationType='RequestResponse',
                Payload=payload.encode('utf-8'),
            )
            logging.info(f'Response from invoke [{response}]')
            return response['Payload'].read()

        except ClientError as e:
            logging.error(e)
            raise e
