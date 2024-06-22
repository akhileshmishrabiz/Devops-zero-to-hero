# SQS Queue Encryption Script

This repository contains a Python script to encrypt unencrypted SQS queues using a specified KMS key across multiple AWS accounts. The script assumes an IAM role in each account to perform the necessary operations.

# Medium blog explaining this automation

https://medium.com/@akhilesh-mishra/python-for-devops-automating-sqs-encryption-for-enhanced-security-641a3d22a958

### Introduction

This Python script is designed to manage Amazon SQS queues and apply server-side encryption using AWS KMS keys across multiple AWS accounts. The script leverages Boto3 to interact with AWS services and assumes IAM roles in specified AWS accounts to gain the necessary permissions. It performs the following key functions:

1. **Assume IAM Role**: Temporarily assumes an IAM role in the specified AWS account to obtain credentials.
2. **List SQS Queues**: Retrieves a list of all SQS queues in the account.
3. **Get Queue Attributes**: Fetches the attributes of each SQS queue, checking for existing encryption.
4. **Encrypt SQS Queue**: Applies server-side encryption to unencrypted SQS queues using a specified KMS key.
5. **Process Accounts**: Scans multiple AWS accounts for unencrypted SQS queues and applies encryption where needed.

The script is executed via command-line arguments, which allow the user to specify the AWS account IDs, IAM role name, and KMS key ID. It processes each account and logs the actions taken, providing error handling to manage any issues that arise during execution. This tool is essential for enhancing the security of SQS queues by ensuring they are encrypted with KMS keys.

## Prerequisites

- Python 3.6+
- Boto3 library
- AWS credentials with the necessary permissions to assume roles and manage SQS queues

## Installation

1. Clone the repository or copy the scripts to your local machine.

2. Install the required Python packages:
    ```sh
    pip install boto3
    ```


