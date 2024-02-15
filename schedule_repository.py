import os
import dynamodb_repository as dynamodb
from botocore.exceptions import ClientError

SCHEDULE_TABLE = os.environ["SCHEDULE_TABLE"]


def insert(schedule):
    try:
        loan_account_table = dynamodb.get_table(SCHEDULE_TABLE)
        loan_account_table.put_item(Item=schedule, ConditionExpression='attribute_not_exists(pk)')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Skip old news")
    except Exception as e:
        print("Error when insert schedule {}".format(e))

