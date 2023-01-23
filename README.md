# AmplifyLogsToS3 v2

An updated v2 of AWS Lambda Function to parse and export AWS Amplify Access Logs onto an S3 bucket. Reads JSON parameters from request event body to allow usage across multiple AWS Amplify deployments, buckets, and regions.

## Build

To build this project from source, [Makefile](./Makefile) is included with `build` and `publish` targets. 

1. Restore dependencies with `make deps` to get started. 
2. Clone [.env]('./include.env') to set deployment name for an existing function. Create a new Lambda function using the AWS CLI before proceeding. 
3. Run `make` to build and publish artifacts to AWS Lambda.

See deployment steps below for IAM and CloudWatch task configuration.

## Request Format

Parameters required to execute lambda function.

```json
{
    "task": {
        "region": "us-east-1",
        "s3_bucket": "bucket-name",
        "domain_name": "amplify-domain-name",
        "app_id": "amplify-app-id"
    }
}
```

## AWS IAM Role Policy

Role policy can be customized and limited to `s3://bucket/prefix` using `ArnLike: sourceArn` of running instance. The default policy uses full access and should only be used for AWS Lambda functions on a private subnet without an attached domain.

`{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSAmplifyAccessLogsExporter",
            "Effect": "Allow",
            "Action": "amplify:*",
            "Resource": "*"
        }
    ]
}`

Deployment of lambda requires attaching `S3FullAccess` and `AWSLambdaBasicExecutionPolicy` to IAM lambda execution role. Permission scopes should be limited appropriately.

## Lambda Requirements 

1. 128MB RAM
2. 2 minute timeout

## CloudWatch CRON Task

Lambda function can be executed automatically every X hours using the following example CRON task. Rules can be created using template provided below, replace parameters `rule-name` `account-id` and `rule-id` `json-payload` appropriately.

```json
> aws events list-rules
{
    "Rules": [
        {
            "Name": "rule-name",
            "Arn": "arn:aws:events:us-east-1:account-id:rule/rule-name",
            "State": "ENABLED",
            "ScheduleExpression": "cron(0 12 * * ? *)",
            "EventBusName": "default"
        }
    ]
}
```

```json
> aws events list-targets-by-rule --rule rule_name 
{
    "Targets": [
        {
            "Id": "rule_id",
            "Arn": "arn:aws:lambda:us-east-1:account-id:function:lambda-function-name",
            "Input": "json-payload"
        }
    ]
}
```

Specify `json-payload` as an inline string for CloudWatch, see [params.json](./params.json) for reference to execute the Lambda function.

Replicate the task in CloudWatch > Events > Rules for every AWS Amplify service to collect and publish logs.

## LICENSE

This project is published under the MIT license, for more information refer to [LICENSE](LICENSE).
