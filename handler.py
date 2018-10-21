from datetime import datetime, timedelta
import json
import boto3

def awss3objectcount(event, context):

    try:
        s3bucketName = event['multiValueQueryStringParameters']['s3BucketName'][0]
    except:
        response = {
            "statusCode": 500,
            "headers": {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Credentials': True,
            },
            "body": "An error occurred. Please contact the Administrator."
        }
        print("ERROR: The parameter s3BucketName was not provided.")
        return response

    s3 = boto3.resource('s3')
    bucketExists = s3.Bucket(s3bucketName) in s3.buckets.all()

    if bucketExists:
        client = boto3.client('cloudwatch')
        response = client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/S3',
                            'MetricName': 'NumberOfObjects',
                            'Dimensions': [
                                {
                                    'Name': 'StorageType',
                                    'Value': 'AllStorageTypes'
                                },
                                {
                                    'Name': 'BucketName',
                                    'Value': s3bucketName
                                },
                            ]
                        },
                        'Period': 3600,
                        'Stat': 'Average',
                        'Unit': 'Count'
                    },
                    'ReturnData': True
                },
            ],
            StartTime=datetime.now() - timedelta(days=1),
            EndTime=datetime.now()
        )

        s3ObjectCount = response['MetricDataResults'][0]['Values'][0]

        body = {
           "s3BucketName": s3bucketName,
           "objectCount": s3ObjectCount
        }

        response = {
            "statusCode": 200,
            "headers": {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Credentials': True,
            },
            "body": json.dumps(body)
        }
    else:
        response = {
            "statusCode": 500,
            "headers": {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Credentials': True,
            },
            "body": "An error occurred. Please contact the Administrator."
        }
        print('ERROR: The S3 bucket ' + s3bucketName + ' was not provided or the S3 connection could not be established.')
    return response
