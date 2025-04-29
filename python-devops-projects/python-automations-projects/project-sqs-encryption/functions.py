# function.py

import boto3
import logging
from botocore.exceptions import ClientError
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def assume_role(account_id: str, role_name: str) -> boto3.Session:
    """
    Assume an IAM role in the specified account and return a Boto3 session.

    :param account_id: AWS account ID to assume the role in.
    :param role_name: Name of the role to assume.
    :return: Boto3 session.
    """
    sts_client = boto3.client('sts')
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="SQSQueueEncryptionSession"
    )
    credentials = response['Credentials']
    return boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

def list_sqs_queues(session: boto3.Session) -> List[str]:
    """
    List all SQS queues in the AWS account using paginators.

    Paginators are a high-level abstraction in Boto3 that allows you to handle responses that are 
    split across multiple pages. This is especially useful for API calls that may return large 
    datasets.

    This function creates a paginator for the `list_queues` operation of the SQS client, which 
    allows it to iterate over all the results pages and collect all the SQS queue URLs.

    :param session: Boto3 session.
    :return: List of SQS queue URLs.
    """
    sqs_client = session.client('sqs')
    paginator = sqs_client.get_paginator('list_queues')
    
    queue_urls = []
    
    # Iterate through each page of results
    for page in paginator.paginate():
        # `page` is a dictionary that contains the response elements.
        # 'QueueUrls' is a key in the response that contains the list of queue URLs.
        queue_urls.extend(page.get('QueueUrls', []))
    
    return queue_urls

def get_queue_attributes(sqs_client, queue_url: str) -> dict:
    """
    Get attributes of a specific SQS queue.

    :param sqs_client: Boto3 SQS client.
    :param queue_url: URL of the SQS queue.
    :return: Dictionary of queue attributes.
    """
    response = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['All']
    )
    return response.get('Attributes', {})

def encrypt_sqs_queue(sqs_client, queue_url: str, kms_key_id: str) -> None:
    """
    Apply server-side encryption to an SQS queue using the specified KMS key.

    :param sqs_client: Boto3 SQS client.
    :param queue_url: URL of the SQS queue.
    :param kms_key_id: KMS key ID to use for encryption.
    """
    sqs_client.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={
            'KmsMasterKeyId': kms_key_id
        }
    )
    logger.info(f"Applied encryption to queue: {queue_url} using KMS key: {kms_key_id}")

def process_account(account_id: str, role_name: str, kms_key_id: str) -> None:
    """
    Process an AWS account by scanning for unencrypted SQS queues and applying encryption.

    :param account_id: AWS account ID.
    :param role_name: IAM role name to assume.
    :param kms_key_id: KMS key ID to use for encryption.
    """
    session = assume_role(account_id, role_name)
    sqs_client = session.client('sqs')
    queue_urls = list_sqs_queues(session)

    for queue_url in queue_urls:
        attributes = get_queue_attributes(sqs_client, queue_url)
        if 'KmsMasterKeyId' not in attributes:
            encrypt_sqs_queue(sqs_client, queue_url, kms_key_id)
