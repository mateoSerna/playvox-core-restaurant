import datetime
import json
import os
import random
import uuid

import boto3
import requests

from api import util

boto3.setup_default_session(region_name="sa-east-1")
dynamodb = boto3.client("dynamodb")
table_name = os.environ["ORDER_TABLE"]
warehouse_api = os.environ["WAREHOUSE_API"]


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        params = {"ingredients": random.choice([2, 3])}
        request = requests.get(f"{warehouse_api}/recipe/random", params=params)

        if request.status_code == requests.codes.ok:
            recipe = request.json()["recipe"]
            if recipe["error"]:
                return {
                    "statusCode": 400,
                    "headers": util.get_response_headers(),
                    "body": json.dumps({"error": recipe["error"]}),
                }
            else:
                item = {
                    "order_id": {"S": str(uuid.uuid4())},
                    "timestamp": {"N": str(datetime.datetime.now().timestamp())},
                    "ingredients": {"SS": recipe["ingredients"]},
                    "status": {"S": "delivered"},
                }
                params = {"TableName": table_name, "Item": item}
                dynamodb.put_item(**params)

                return {
                    "statusCode": 200,
                    "headers": util.get_response_headers(),
                    "body": json.dumps(item),
                }
        else:
            return {
                "statusCode": 400,
                "headers": util.get_response_headers(),
                "body": json.dumps({"error": "Error getting the recipe."}),
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": util.get_response_headers(),
            "body": json.dumps({"error": str(e)}),
        }
