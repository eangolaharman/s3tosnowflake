import json

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name):
    # Create a Secrets Manager Client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Error while retrieving client secret from aws secret manager: {e}")
        raise e

    secret = get_secret_value_response['SecretString']
    try:
        secret_dict = json.loads(secret)
        return secret_dict
    except Exception as e:
        return secret
