import uuid
import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

s3 = boto3.client("s3")

table = dynamodb.Table('Project2Users')

def lambda_handler(event, context):
    username = event["queryStringParameters"]["username"].lower()
    file_key = event["queryStringParameters"]["filename"]

    http_res = {}
    http_res["statusCode"] = 200
    http_res["headers"] = {}
    http_res["headers"]["Content-Type"] = "application/json"

    user_id = validate_username(username)
    if user_id == None:
        res_body = {"status":"error", "message":"We do not have a user matching that username, please create an account and try again"}
        http_res["body"] = res_body
        return http_res
    
    #Get the file contents
    contents = get_contents(user_id, file_key)

    if contents == None:
        res_body = {"status":"error", "message":"The file you are trying to download does not exist"}

    http_res["body"] = contents
    return http_res

def validate_username(username):
    
    res = table.scan(ScanFilter = {"username":{"AttributeValueList":[username], "ComparisonOperator":"EQ"}})
    if res["Count"] == 1:
        return res["Items"][0]["UserID"]
    
    return None

def get_contents(UID, file_key):
    try:
        obj = s3.get_object(Bucket="mcproject2post", Key=f"{UID}/{file_key}")
    except:
        return None
    return obj["Body"].read().decode("utf-8")