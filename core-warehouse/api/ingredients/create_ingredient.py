import datetime
import json
import os
import uuid

import boto3

from api import util

boto3.setup_default_session(region_name="sa-east-1")
dynamodb = boto3.client("dynamodb")
table_name = os.environ["INGREDIENT_TABLE"]


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        item = json.loads(event["body"])["Item"]
        for item_key in item.keys():
            item[item_key] = {"S": item[item_key]}

        item["ingredient_id"] = {"S": str(uuid.uuid4())}
        item["timestamp"] = {"N": str(datetime.datetime.now().timestamp())}

        if "is_active" not in item:
            item["is_active"] = {"S": "active"}

        params = {"TableName": table_name, "Item": item}
        dynamodb.put_item(**params)

        return {
            "statusCode": 200,
            "headers": util.get_response_headers(),
            "body": json.dumps(item),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": util.get_response_headers(),
            "body": json.dumps({"error": str(e)}),
        }
