import json

import boto3
from botocore.exceptions import ClientError


class Lambda:
    """
    The client of AWS Lambda
    """
    _client = {}

    @classmethod
    def _get_client(cls, region: str):
        if region not in cls._client:
            session = boto3.session.Session()
            cls._client[region] = session.client(
                service_name='lambda',
                region_name=region
            )
        return cls._client[region]

    @classmethod
    def invoke(cls, region: str, arn: str, payload: str):
        """
        Invokes a Lambda function

        :return:
        """
        if not region:
            raise ValueError(u'region is required')

        if not arn:
            raise ValueError(u'arn is required')

        try:
            response = cls._get_client(region).invoke(
                FunctionName=arn,
                InvocationType='RequestResponse',
                Payload=payload.encode('utf-8'),
            )
            return response['Payload'].read()

        except ClientError as e:
            print(e)
            raise e


def _process_message(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'text/html',
    }

    # with requests.get(url, stream=True, allow_redirects=True, headers=headers) as response:
    #     if response.status_code != 200:
    #         print(f'Getting URL "{url}" resulted in status code {response.status_code}')
    #         raise Exception
    #
    #     print(f'Original URL {url}, final URL {response.url}')
    #
    #     print(response.url)
    #     print(response.content)

    # http = urllib3.PoolManager()
    # response = http.request('GET', url, headers=headers)
    #
    # print({
    #     'statusCode': response.status,
    #     'url': response.geturl(),
    #     'content': response.data
    # })

    r = Lambda.invoke('us-east-1', 'arn:aws:lambda:us-east-1:430714039810:function:download', json.dumps({'url': 'https://ca.indeed.com/rc/clk?jk=e6c34332dcf5a31b&fccid=a499083ea4884469&vjs=3'}))
    print(json.loads(r))


if __name__ == '__main__':
    _process_message('https://ca.indeed.com/rc/clk?jk=68c29bf549e90565&fccid=354f4c12e3c6bd5a&vjs=3')
