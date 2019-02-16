# AWS S3 Object Count

With this solution, you can check the object count of an AWS S3 Bucket via HTTP API.

You can use this HTTP endpoint to integrate the object count in a monitor system. It can be used to check S3 replication for example.

## Requirements

* Python 3 (tested with version 3.7.0)
* Node.js (tested with version 10.15.1)
* Serverless (tested with version 1.37.1)
* Serverless Plugins
  * AWS Pseudo Parameters (install via ```npm install serverless-pseudo-parameters```)
  * serverless plugin tracing (install via ```npm install serverless-plugin-tracing```)
  * serverless-api-gateway-xray plugin (install via npm install serverless-api-gateway-xray)

## Deploy the solution

1. Clone this repository
2. Deploy the solution to AWS with ```sls deploy```. Please note the API-ID and the X-API-Key in the output
3. Test the endpoint via ```curl -X GET 'https://<<gateway id>>.execute-api.<<region>>.amazonaws.com/dev/?s3BucketName=<<<bucket-name>>>' --header "X-Api-Key:<<<API-Key>>>"```

### Undeploy the solution

Just follow the next steps to undeploy the solution:

1. run ```sls remove``` to remove the solution
