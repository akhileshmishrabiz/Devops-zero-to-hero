import argparse
import logging
from functions import process_account

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Encrypt unencrypted SQS queues across multiple AWS accounts.")
    parser.add_argument('--accounts', '-a', nargs='+', required=True, help="List of AWS account IDs.")
    parser.add_argument('--role-name', '-r', required=True, help="Name of the IAM role to assume in each account.")
    parser.add_argument('--kms-key-id', '-k', required=True, help="KMS key ID to use for encryption.")
    args = parser.parse_args()

    for account_id in args.accounts:
        try:
            logger.info(f"Processing account: {account_id}")
            process_account(account_id, args.role_name, args.kms_key_id)
        except Exception as e:
            logger.error(f"Failed to process account {account_id}: {e}")

if __name__ == "__main__":
    main()
