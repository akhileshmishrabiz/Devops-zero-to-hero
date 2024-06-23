import boto3
import argparse
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_lambda_functions():
    """
    List all Lambda functions in the AWS account using pagination.

    :return: List of Lambda functions.
    """
    client = boto3.client('lambda')
    paginator = client.get_paginator('list_functions')
    lambda_functions = []

    # Paginate through all Lambda functions
    for page in paginator.paginate():
        lambda_functions.extend(page['Functions'])
    
    return lambda_functions

def update_lambda_runtime(function_name, current_runtime, new_runtime):
    """
    Update the runtime of a specified Lambda function.

    :param function_name: Name of the Lambda function.
    :param current_runtime: Current runtime of the Lambda function.
    :param new_runtime: Desired runtime to update to.
    """
    client = boto3.client('lambda')
    try:
        client.update_function_configuration(
            FunctionName=function_name,
            Runtime=new_runtime
        )
        logger.info(f"Updated {function_name} from {current_runtime} to {new_runtime}")
    except Exception as e:
        logger.error(f"Failed to update {function_name} from {current_runtime} to {new_runtime}: {e}")

def main(desired_python_version, desired_nodejs_version):
    """
    Main function to list and update Lambda runtimes to desired versions.

    :param desired_python_version: Desired Python runtime version (e.g., python3.9).
    :param desired_nodejs_version: Desired NodeJS runtime version (e.g., nodejs14.x).
    """
    lambdas = list_lambda_functions()

    # Iterate over all Lambda functions
    for function in lambdas:
        runtime = function['Runtime']
        function_name = function['FunctionName']

        # Check if the runtime is an older version of Python
        if runtime.startswith('python') and runtime < desired_python_version:
            update_lambda_runtime(function_name, runtime, desired_python_version)
        # Check if the runtime is an older version of NodeJS
        elif runtime.startswith('nodejs') and runtime < desired_nodejs_version:
            update_lambda_runtime(function_name, runtime, desired_nodejs_version)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update AWS Lambda runtimes to desired versions.")
    parser.add_argument('--python-version', type=str, required=True, help="Desired Python runtime version (e.g., python3.9)")
    parser.add_argument('--nodejs-version', type=str, required=True, help="Desired NodeJS runtime version (e.g., nodejs14.x)")

    args = parser.parse_args()

    main(args.python_version, args.nodejs_version)
