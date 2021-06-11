import json
import os

import boto3

from api import util

boto3.setup_default_session(region_name="sa-east-1")
dynamodb = boto3.client("dynamodb")
table_name = os.environ["INGREDIENT_TABLE"]


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        item = json.loads(event["body"])["Item"]
        timestamp = item.get("timestamp")
        for item_key in item.keys():
            item[item_key] = {"S": item[item_key]}

        if "ingredients" in item:
            item["ingredients"] = {"SS": item["ingredients"]}
        if timestamp:
            item["timestamp"] = {"N": timestamp}

        params = {
            "TableName": table_name,
            "Item": item,
            "ConditionExpression": "#recipe_id = :recipe_id",
            "ExpressionAttributeNames": {"#recipe_id": "recipe_id"},
            "ExpressionAttributeValues": {":recipe_id": item["recipe_id"]},
        }
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
