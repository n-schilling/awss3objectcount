import json
import boto3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_resource = boto3.resource('s3')
cloudwatch_client = boto3.client('cloudwatch')

error_response = {
    "statusCode": 500,
    "headers": {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': True,
    },
    "body": "An error occurred. Please contact the Administrator."
}

def getS3ObjectCountFromCloudWatch(s3bucketName):
    logger.info('getS3ObjectCountFromCloudWatch for bucket ' + s3bucketName)
    get_metric_data_response = cloudwatch_client.get_metric_data(
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

    s3ObjectCount = get_metric_data_response['MetricDataResults'][0]['Values'][0]
    logger.info('Found ' + str(s3ObjectCount) + ' objects in the bucket')
    return s3ObjectCount

def checkS3BucketExists(s3bucketName):
    logger.info('checkS3BucketExists for bucket ' + s3bucketName)
    bucketExists = s3_resource.Bucket(s3bucketName) in s3_resource.buckets.all()
    return bucketExists

def awss3objectcount(event, context):
    try:
        s3bucketName = event['multiValueQueryStringParameters']['s3BucketName'][0]
    except:
        logger.error("The parameter s3BucketName was not provided in the event.")
        return error_response
    try:
        bucketExists = checkS3BucketExists(s3bucketName)
    except:
        logger.error("Could not check if the bucket exists")
        return error_response

    if bucketExists:
        try:
            s3ObjectCount = getS3ObjectCountFromCloudWatch(s3bucketName)
        except:
            logger.error("Could not retrieve s3 object count from cloudwatch")
            return error_response

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
        return response
    else:
        logger.error('The S3 bucket ' + s3bucketName + ' was not provided or the S3 connection could not be established.')
    return error_response
