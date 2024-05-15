import uuid
import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

s3 = boto3.client("s3")

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
        http_res["body"] = {"status":"error", "message":"There is no account assigned to that username"}
        return http_res

    file_key = event["queryStringParameters"]["filename"]

    res = delete_file(UID, file_key)
    if res == None:
        http_res["body"] = {"status":"error", "message":"The file that you indicated does not exist"}
        return http_res

    http_res["body"] = json.dumps({"status":"success", "message":"The file was successfully deleted"})
    return http_res


def validate_username(username):
    
    res = table.scan(ScanFilter = {"username":{"AttributeValueList":[username], "ComparisonOperator":"EQ"}})
    if res["Count"] == 1:
        return res["Items"][0]["UserID"]
    
    return None

def delete_file(UID, file_key):
    file_list = [obj.key.split(f"{UID}/")[1] for obj in bucket.objects.all() if (obj.key.startswith(f"{UID}/") and obj.key != f"{UID}/")]
    if file_key not in file_list:
        return None
    #Bucket should be like post. Key should be user provided. 
    s3.delete_object(Bucket="mcproject2post", Key=f"{UID}/{file_key}")
    return "Deleted"