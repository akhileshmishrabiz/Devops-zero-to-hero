# AWS Lambda Runtime Updater
This Python script lists AWS Lambda functions running older versions of Python and NodeJS runtimes and updates them to specified newer versions. It leverages the AWS Boto3 library to interact with AWS Lambda, using pagination to handle large sets of Lambda functions.

# Medium Blog explaining the automation
https://medium.com/@akhilesh-mishra/automate-outdated-aws-lambda-runtime-updates-752ec4dc9fd4


Requirements

Python 3.6+
Boto3

AWS credentials with permissions to list and update Lambda functions

Installation
Clone the repository:

git clone https://github.com/akhileshmishrabiz/Devops-zero-to-hero.git

cd python-project-2


# Install the required Python packages:
pip install boto3 # or pip install -r requirements.txt

# Usage

python update_lambda_runtimes.py --python-version python3.9 --nodejs-version nodejs14.x

# Arguments

--python-version: The desired Python runtime version (e.g., python3.9).

--nodejs-version: The desired NodeJS runtime version (e.g., nodejs14.x).

# Example

python update_lambda_runtimes.py --python-version python3.9 --nodejs-version nodejs14.x

This command will update all Lambda functions running older versions of Python or NodeJS to the specified newer versions.

