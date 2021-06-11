import json
import os

import boto3

from api import util

boto3.setup_default_session(region_name="sa-east-1")
dynamodb = boto3.client("dynamodb")
table_name = os.environ["ORDER_TABLE"]


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        params = {
            "TableName": table_name,
            "IndexName": "status-index",
            "KeyConditionExpression": "#s = :s",
            "ExpressionAttributeNames": {"#s": "status"},
            "ExpressionAttributeValues": {":s": {"S": "delivered"}},
            "ScanIndexForward": False,
        }
        data = dynamodb.query(**params)

        return {
            "statusCode": 200,
            "headers": util.get_response_headers(),
            "body": json.dumps(data),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": util.get_response_headers(),
            "body": json.dumps({"error": str(e)}),
        }
