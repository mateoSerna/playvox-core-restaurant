import json
import os
import random

import boto3

from api import util

boto3.setup_default_session(region_name="sa-east-1")
dynamodb = boto3.client("dynamodb")
table_name = os.environ["INGREDIENT_TABLE"]


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        query = event["queryStringParameters"]
        quantity_ingredients = int(query.get("ingredients")) if query else 3
        ingredients = get_ingredients(quantity=quantity_ingredients)

        return {
            "statusCode": 200,
            "headers": util.get_response_headers(),
            "body": json.dumps({"recipe": ingredients}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": util.get_response_headers(),
            "body": json.dumps({"error": str(e)}),
        }


def get_ingredients(quantity: int) -> dict:
    response = {"error": None, "ingredients": []}

    try:
        ingredients = []
        params = {
            "TableName": table_name,
            "IndexName": "is_active-index",
            "KeyConditionExpression": "is_active = :is_active",
            "ExpressionAttributeValues": {":is_active": {"S": "active"}},
            "ScanIndexForward": False,
        }
        items = dynamodb.query(**params)

        if items["Count"] >= quantity:
            selected_items = random.sample(items["Items"], quantity)
            ingredients = [item["name"]["S"] for item in selected_items]

            response["ingredients"] = ingredients
        else:
            response["error"] = "There are not enough ingredients."
    except Exception as e:
        response["error"] = str(e)

    return response
