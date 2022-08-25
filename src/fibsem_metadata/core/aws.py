import json
import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional, TypedDict

AWS_REGION = 'us-east-1'
AWS_DB_SECRET_NAME = 'AWS_DB_SECRET_NAME'

class AwsDatabaseSecret(TypedDict):
    password: str
    username: str
    host: str
    dbname: str
    port: int


def on_lambda() -> bool:
    return os.environ.get("AWS_EXECUTION_ENV") is not None


def _get_secret(secret_name: str,
                region: str = AWS_REGION) -> AwsDatabaseSecret:
    """
    Retrieve a secret from the aws secretsmanager using a secret name
    """

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']

    return json.loads(secret)


def get_database_secret(aws_region=AWS_REGION,
                        secret_env_var=AWS_DB_SECRET_NAME) -> Optional[AwsDatabaseSecret]:

    database_secret = None
    secret_string = os.environ.get(secret_env_var)

    if secret_string is not None:
        database_secret = _get_secret(secret_string, aws_region)

    return database_secret
