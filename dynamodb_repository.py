import os

import boto3
from botocore.config import Config as BotoCfg

DYNAMO_DB_SERVICE = "dynamodb"
TABLE_REGION = os.environ["TABLE_REGION"]

dynamodb_client = boto3.resource(DYNAMO_DB_SERVICE, region_name=TABLE_REGION, config=BotoCfg(retries={"mode": "standard"}))

_DYNAMODB_CONFIG = {}


def get_table(table_name: str):
    if table_name not in _DYNAMODB_CONFIG:
        _DYNAMODB_CONFIG[table_name] = dynamodb_client.Table(table_name)
    return _DYNAMODB_CONFIG[table_name]
