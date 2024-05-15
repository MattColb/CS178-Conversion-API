import uuid
import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

bucket = boto3.Session().resource("s3").Bucket("mcproject2post")

table = dynamodb.Table('Project2Users')

def lambda_handler(event, context):
    username = event["queryStringParameters"]["username"].lower()

    http_res = {}
    http_res["statusCode"] = 200
    http_res["headers"] = {}
    http_res["headers"]["Content-Type"] = "application/json"
    

    UID = validate_username(username)
    if UID == None:
        res_body = {"status":"error", "message":"There is no account that is associated with that username."}
        http_res["body"] = json.dumps(res_body)

    files = get_files(UID)
    http_res["body"] = json.dumps({"status":"success", "files":files})
    return http_res


def validate_username(username):
    
    res = table.scan(ScanFilter = {"username":{"AttributeValueList":[username], "ComparisonOperator":"EQ"}})
    if res["Count"] == 1:
        return res["Items"][0]["UserID"]
    
    return None

def get_files(UID):
    file_list = [obj.key.split(f"{UID}/")[1] for obj in bucket.objects.all() if (obj.key.startswith(f"{UID}/") and obj.key != f"{UID}/")]
    return file_list