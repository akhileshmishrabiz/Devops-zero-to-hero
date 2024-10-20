Terraform To Deploy AWS Lambda Function With S3 Trigger

# Blog 

https://medium.com/@akhilesh-mishra/terraform-to-deploy-aws-lambda-function-with-s3-trigger-4c8e231d5f0c

# Implementation

I will use Terraform to provision the Lambda function.

I will use Python as Lambda runtime.

Python script will pick the files uploaded to a path and move them to their respective folder with year, month, and date.

S3 notification will trigger the Lambda (When any new files get uploaded to the bucket on a path)
