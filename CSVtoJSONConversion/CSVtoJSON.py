import csv
import json
from urllib.parse import unquote_plus
import io
import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    file_obj = event["Records"][0]
    bucketname = str(file_obj["s3"]["bucket"]["name"])
    filename = unquote_plus(str(file_obj["s3"]["object"]["key"]))
    write_to_json(bucketname, filename)
    
def write_to_json(bucketname, filename):
    obj = s3.get_object(Bucket=bucketname, Key=filename)
    f = filename.split(".")
    f[-1] = "json"
    new_filename = ".".join(f)
    print(new_filename)
    with io.BytesIO(obj["Body"].read()) as csvfile:
        reader = csv.DictReader(io.TextIOWrapper(csvfile, encoding='utf-8'))
        data = [row for row in reader]
    s3.put_object(Bucket = "mcproject2post", Key=new_filename, Body = (bytes(json.dumps(data).encode('UTF-8'))))
    