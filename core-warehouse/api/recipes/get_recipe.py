import json
import os

import boto3

from api import util

boto3.setup_default_session(region_name="sa-east-1")
dynamodb = boto3.client("dynamodb")
table_name = os.environ["INGREDIENT_TABLE"]


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        recipe_id = event["pathParameters"]["recipe_id"]
        params = {
            "TableName": table_name,
            "KeyConditionExpression": "recipe_id = :recipe_id",
            "ExpressionAttributeValues": {":recipe_id": {"S": recipe_id}},
            "Limit": 1,
        }
        data = dynamodb.query(**params)

        if data.get("Items"):
            return {
                "statusCode": 200,
                "headers": util.get_response_headers(),
                "body": json.dumps(data["Items"][0]),
            }
        else:
            return {"statusCode": 404, "headers": util.get_response_headers()}
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": util.get_response_headers(),
            "body": json.dumps({"error": str(e)}),
        }
