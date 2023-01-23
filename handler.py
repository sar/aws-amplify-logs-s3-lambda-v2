import json
import boto3
import urllib.request
from time import gmtime, strftime

def lambda_handler(event, context):
    payload = event["body"]
    if payload is None:
        raise ValueError("[err]::missing_req_params")

    params = json.load(payload)
    print(params)

    REGION = params["region"];
    BUCKET_NAME = params["bucket_name"];
    APP_ID = params["app_id"];
    DOMAIN_NAME = params["domain_name"];

    TIME_STAMP = strftime("%Y_%m_%d_%H%M%S", gmtime())
    FILE_NAME = str(TIME_STAMP + '_' + 'access_logs' + '_' + DOMAIN_NAME)

    client = boto3.client('amplify')
    response = client.generate_access_logs(
        domainName=DOMAIN_NAME,
        appId=APP_ID
    )

    if response is None:
        raise ValueError("[err]::empty_resp::" + DOMAIN_NAME)

    logUrl = response['logUrl']

    urllib.request.urlretrieve(logUrl, '/tmp/' + FILE_NAME)

    s3_client = boto3.client("s3", region_name=REGION)
    s3_client.upload_file('/tmp/' + FILE_NAME, BUCKET_NAME, FILE_NAME + '.csv')
    s3_uri = "s3://" + BUCKET_NAME + "/" + FILE_NAME + ".csv"

    return {
        'statusCode': 200,
        'body': json.dumps("[200]::s3_client_write_ok::" + s3_uri)
    }
