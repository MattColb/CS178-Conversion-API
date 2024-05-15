import uuid
import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

s3 = boto3.client("s3")

table = dynamodb.Table('Project2Users')

def lambda_handler(event, context):
    username = event["queryStringParameters"]["username"]

    res_body = generate_user(username)

    http_res = {}
    http_res["statusCode"] = 200
    http_res["headers"] = {}
    http_res["headers"]["Content-Type"] = "application/json"
    http_res["body"] = json.dumps(res_body)
    return http_res

def generate_user(username):
    #Check if username is in the table, if it is, return {}, user was not created, try a different username
    username = username.lower()
    res = table.scan(ScanFilter = {"username":{"AttributeValueList":[username], "ComparisonOperator":"EQ"}})
    if res["Count"] == 1:
        return {"status":"error","message":"This username is already taken, please try using a different one"}

    user_id = str(uuid.uuid4())
    #put the item in the table
    table.put_item(
        Item={
            "UserID": user_id,
            "username": username
        }
    )

    s3.put_object(Bucket="mcproject2pre", Key=user_id+'/')
    s3.put_object(Bucket="mcproject2post", Key=user_id+'/')
    return {"status":"success", "message":"User has been successfully created", "UserID":user_id, "username":username}

