import boto3  # Import the Boto3 library for interacting with AWS services.
from packaging.version import Version  # Import the Version class for version parsing and comparison.
import argparse  # Import the argparse module for parsing command-line arguments.
from typing import Optional, List, Dict, Any  # Import type hints for optional, list, dictionary, and any types.
import logging  # Import the logging module for logging messages.
import colorlog  # Import the colorlog module for colored logging output.


# Create a Lambda client
lambda_client = boto3.client('lambda')


def parse_arguments():
    parser = argparse.ArgumentParser(description="Encrypt unencrypted SQS queues across multiple AWS accounts.")
    parser.add_argument('--python_version', '-a', required=True, help="List of AWS account IDs.")
    return  parser.parse_args()
def list_lambda_functions() -> Optional[List[Dict[str, Any]]]:
    """
    List all AWS Lambda functions in the account.

    :return: A list of dictionaries containing Lambda function details, or None if not found.
    """
    return lambda_client.list_functions().get("Functions", None)

def get_name_runtime(lambda_json_list: List[Dict[str, Any]]) -> List[tuple]:
    """
    Extract function names and runtimes from a list of Lambda function details.

    :param lambda_json_list: A list of dictionaries with Lambda function details.
    :return: A list of tuples containing function names and runtimes.
    """
    temp = []
    for item in lambda_json_list:
        name = item.get("FunctionName", "")
        runtime = item.get("Runtime", None)
        if runtime:
            temp.append((name, runtime))
    return temp

def compare_runtime(runtime: str, runtime_to_compare_with: str) -> bool:
    """
    Compare two Python runtimes to check if the first is older than the second.

    :param runtime: The current runtime version string.
    :param runtime_to_compare_with: The runtime version string to compare against.
    :return: True if the current runtime is older, otherwise False.
    """
    return Version(runtime.split("python")[-1]) < Version(runtime_to_compare_with.split("python")[-1])

def update_runtime(function_name: str, old_runtime: str, new_runtime: str) -> None:
    """
    Update the runtime of a specified Lambda function.

    :param function_name: The name of the Lambda function to update.
    :param old_runtime: The current runtime of the function.
    :param new_runtime: The new runtime to set for the function.
    """
    logging.info(f'Updating {function_name} runtime from {old_runtime} to {new_runtime}')
    try:
        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Runtime=new_runtime
        )
    except Exception as e:
        logging.error("An error occurred while updating the runtime")

def apply_logs() -> None:
    """
    Apply logging configuration with color coding.
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    logger = colorlog.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def run(runtime_to_compare_with: str) -> None:
    """
    Update all Lambda functions to a specified runtime if their current runtime is older.

    :param runtime_to_compare_with: The runtime version string to compare against.
    """
    apply_logs()

    data = get_name_runtime(list_lambda_functions() or [])
    temp = []
    for item in data:
        name, runtime = item
        if compare_runtime(runtime, runtime_to_compare_with):
            temp.append(name)
            update_runtime(name, runtime, runtime_to_compare_with)
    if not temp:
        logging.info(f"No functions with runtime older than {runtime_to_compare_with}")

if __name__ == "__main__":
    args=parse_arguments()
    runtime_to_compare_with =args.python_version
    run(runtime_to_compare_with)

