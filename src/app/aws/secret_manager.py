import logging

import boto3
import base64
from botocore.exceptions import ClientError

import config


class SecretManager:
    """
    The client of AWS Secret Manager
    """
    _client = None

    @classmethod
    def _get_client(cls):
        if not cls._client:
            session = boto3.session.Session()
            cls._client = session.client(
                service_name='secretsmanager',
                region_name=config.AWS_REGION
            )
        return cls._client

    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    @classmethod
    def get_secret(cls, secret_name):
        try:
            get_secret_value_response = cls._get_client().get_secret_value(
                SecretId=secret_name
            )
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                return secret
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                return decoded_binary_secret

        except ClientError as e:
            logging.error(e)
            raise e
