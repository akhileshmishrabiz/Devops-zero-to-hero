import boto3  # Import the Boto3 library for interacting with AWS services.
from packaging.version import Version  # Import the Version class for version parsing and comparison.
import argparse  # Import the argparse module for parsing command-line arguments.


# Create a Lambda client
lambda_client = boto3.client('lambda')

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description=" take python version as input")
    parser.add_argument('--python_version', '-a', required=True, help=" Python version")
    return parser.parse_args()

# List all AWS Lambda functions in the account
def list_lambda_functions():
    return lambda_client.list_functions().get("Functions", None)


# Extract function names and runtimes from Lambda function details
def get_name_runtime(lambda_json_list):
    temp = []
    for item in lambda_json_list:
        name = item.get("FunctionName", "")
        runtime = item.get("Runtime", None)
        if runtime:
            temp.append((name, runtime))
    return temp

# Compare two Python runtimes to check if the first is older
def compare_runtime(runtime, runtime_to_compare_with):
    return Version(runtime.split("python")[-1]) < Version(runtime_to_compare_with.split("python")[-1])

# Update the runtime of a specified Lambda function
def update_runtime(function_name, old_runtime, new_runtime):
    print(f'Updating {function_name} runtime from {old_runtime} to {new_runtime}')
    try:
        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Runtime=new_runtime
        )
    except Exception as e:
        print("An error occurred while updating the runtime")


# Update all Lambda functions to a specified runtime if their current runtime is older
def run(runtime_to_compare_with):

    data = get_name_runtime(list_lambda_functions() or [])
    temp = []
    for item in data:
        name, runtime = item
        if compare_runtime(runtime, runtime_to_compare_with):
            temp.append(name)
            update_runtime(name, runtime, runtime_to_compare_with)
    if not temp:
        print(f"No functions with runtime older than {runtime_to_compare_with}")

if __name__ == "__main__":
    args = parse_arguments()
    runtime_to_compare_with = args.python_version
    run(runtime_to_compare_with)

