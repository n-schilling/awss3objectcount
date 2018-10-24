# AWS S3 Object Count

With this code snipped you can check the object count of an AWS S3 Bucket via HTTP API. For production use you should think about authentication at the HTTP endpoint.

You can use this HTTP endpoint to integrate the object count in a monitor system. It can be used to check S3 replication for example.

## Requirements

* Python 3 (tested with version 3.7.0)
* Node.js (tested with version 8.12.0)
* Serverless (tested with version 1.32.0)
* AWS Pseudo Parameters (install via ```npm install serverless-pseudo-parameters```)
* serverless plugin tracing (install via ```npm install serverless-plugin-tracing```)

## How to install

1. Clone this repository
2. Deploy the solution to AWS with ```sls deploy```. Please note the API-ID and the X-API-Key in the output
3. Test the endpoint via ```curl -X GET 'https://<<gateway id>>.execute-api.<<region>>.amazonaws.com/dev/?s3BucketName=<<<bucket-name>>>' --header "X-Api-Key:<<<API-Key>>>"```
