import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Employees")


def decimal_to_number(value):
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    return value


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    path_parameters = event.get("pathParameters") or {}
    employee_id = path_parameters.get("id")

    if not employee_id:
        return response(
            400,
            {"error": "Employee ID is required"}
        )

    result = table.get_item(
        Key={
            "EmployeeID": employee_id
        }
    )

    item = result.get("Item")

    if not item:
        return response(
            404,
            {"error": "Employee not found"}
        )

    employee = {
        "employeeId": item["EmployeeID"],
        "name": item["Name"],
        "salary": decimal_to_number(item["Salary"]),
        "dateOfJoin": item["DateOfJoin"],
        "description": item["Description"]
    }

    return response(200, employee)