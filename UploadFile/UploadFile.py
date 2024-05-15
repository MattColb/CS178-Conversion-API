import uuid
import boto3
import base64
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

s3 = boto3.client("s3")

table = dynamodb.Table('Project2Users')

conversion_table = dynamodb.Table('Conversions')

def lambda_handler(event, context):
    print(event)
    #Pull out username and validate it
    username = event["queryStringParameters"]["username"].lower()
    toType = event["queryStringParameters"].get("toType", False)
    if toType:
        toType = toType.upper()

    http_res = {}
    http_res["statusCode"] = 200
    http_res["headers"] = {}
    http_res["headers"]["Content-Type"] = "application/json"

    user_id = validate_username(username)
    if user_id == None:
        res_body = {"status":"error", "message":"We do not have a user matching that username, please create an account and try again"}
        http_res["body"] = res_body
        return http_res
    
    #Switch to pull out the binary file and get the filename (to upload)
    body = event["body"]
    contents = base64.b64decode(body)
    f = contents.split(b"\r\n\r\n")[0].split(b"\r\n")[1].split(b";")[-1].split(b'"')[-2]
    filename = f.decode("utf-8")
    print(filename)
    contents = contents.split(b"\r\n\r\n")[1]
    
    if toType == False:
        #Post the file into the post bucket and return that it has been successfully uploaded
        s3.put_object(Bucket="mcproject2post", Key=f"{user_id}/{filename}", Body=contents)
        res_body = {"status":"success", "message":"Your file has been successfully uploaded"}
        http_res["body"] = json.dumps(res_body)
        return res_body

    #Pull out file format from
    fromType= filename.split(".")[-1].upper()
    
    valid_type = check_valid_conversion(fromType, toType)
    if valid_type == False:
        res_body = {"status":"error", "message":"We do not currently support this type of file conversion"}
        http_res["body"] = res_body
        return res_body
        
    upload_file(user_id, toType, filename, contents)

    res_body = {"status":"success", "message":"Your file has been successfully uploaded"}
    http_res["body"] = json.dumps(res_body)
    return http_res    
    

def validate_username(username):
    
    res = table.scan(ScanFilter = {"username":{"AttributeValueList":[username], "ComparisonOperator":"EQ"}})
    if res["Count"] == 1:
        return res["Items"][0]["UserID"]
    
    return None

def check_valid_conversion(fromType, toType):
    res = conversion_table.scan(ScanFilter = {"toType":{"AttributeValueList":[toType], "ComparisonOperator":"EQ"}, 
                                              "fromType":{"AttributeValueList":[fromType], "ComparisonOperator":"EQ"}})
    return res["Count"] == 1

#contents will be the contents of the file
def upload_file(UID, toType, filename, contents):

    #Change so that toType is in between the UID and filename for more functionality. May result in duplicates in the post s3. 
    s3.put_object(Bucket="mcproject2pre", Key=f"{UID}/{filename}", Body=contents)