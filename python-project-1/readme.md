# SQS Queue Encryption Script
This Python script uses the AWS SDK for Python (Boto3) to manage encryption for AWS SQS (Simple Queue Service) queues. The script performs the following tasks:

Lists all SQS queue URLs in the AWS account.

Identifies which queues are not encrypted.

Encrypts the unencrypted queues using a specified KMS (Key Management Service) key.

# Prerequisites
Before using this script, ensure you have the following:

AWS Account: Access to an AWS account with the necessary permissions to manage SQS queues and KMS keys.

AWS CLI Configuration: AWS CLI should be configured with the appropriate credentials.

aws configure
Boto3: The AWS SDK for Python should be installed.

pip install boto3

Usage
Functions
list_queue_urls

Lists all SQS queue URLs in the AWS account.
Returns: A list of queue URLs.
get_kms_key

Retrieves the KMS key ID associated with a given SQS queue URL.

Parameters:
queue_url (str): The URL of the SQS queue.

Returns: The KMS key ID if the queue is encrypted, otherwise None.
queue_without_encryption

Identifies SQS queues that are not encrypted.
Returns: A list of URLs of SQS queues without encryption.

encrypt_queue

Encrypts a given SQS queue with the specified KMS key.

Parameters:
queue_url (str): The URL of the SQS queue to encrypt.
kms_key (str): The KMS key ID to use for encryption.
Returns: The response from the set_queue_attributes call.
run

Encrypts all unencrypted SQS queues with the specified KMS key.

Parameters:
kms_key (str): The KMS key ID to use for encryption.
