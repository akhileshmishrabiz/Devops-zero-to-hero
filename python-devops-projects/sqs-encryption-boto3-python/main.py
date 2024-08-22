import boto3

# Create an SQS client
sqs = boto3.client("sqs")

def list_queue_urls():
    """
    List all SQS queue URLs in the AWS account.

    :return: A list of queue URLs.
    """
    return sqs.list_queues()["QueueUrls"]

def get_kms_key(queue_url):
    """
    Get the KMS key ID associated with the given SQS queue URL.

    :param queue_url: The URL of the SQS queue.
    :return: The KMS key ID if the queue is encrypted, otherwise None.
    """
    try:
        # Get the queue attributes
        response = sqs.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["KmsMasterKeyId"]
        )
        return response["Attributes"]["KmsMasterKeyId"]
    except Exception as e:
        # Return None if any error occurs
        # print(f"some error happened \n{e}")
        return None

def queue_without_encryption():
    """
    Identify SQS queues that are not encrypted.

    :return: A list of URLs of SQS queues without encryption.
    """
    queue_without_encryption = []
    for queue_url in list_queue_urls():
        kms = get_kms_key(queue_url)
        if not kms:
            queue_without_encryption.append(queue_url)
    return queue_without_encryption

def encrypt_queue(queue_url, kms_key):
    """
    Encrypt the given SQS queue with the specified KMS key.

    :param queue_url: The URL of the SQS queue to encrypt.
    :param kms_key: The KMS key ID to use for encryption.
    :return: The response from the set_queue_attributes call.
    """
    response = sqs.set_queue_attributes(
        QueueUrl=queue_url, Attributes={"KmsMasterKeyId": kms_key}
    )
    return response

def run(kms_key):
    """
    Encrypt all unencrypted SQS queues with the specified KMS key.

    :param kms_key: The KMS key ID to use for encryption.
    """
    for item in queue_without_encryption():
        encrypt_queue(item, kms_key)


if __name__ == "__main__":
    kms_key = "your-key-id"  # or alias/alias_name
    run(kms_key)
