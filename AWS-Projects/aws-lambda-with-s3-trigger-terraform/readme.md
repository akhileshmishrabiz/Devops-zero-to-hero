# AWS Lambda with S3 Trigger using Terraform

This project demonstrates how to deploy an AWS Lambda function that automatically organizes files in S3 buckets based on their timestamps using Terraform.

## Blog post
https://livingdevops.com/devops/terraform-to-deploy-aws-lambda-function-with-s3-trigger/

## 🎯 Project Overview

When files with date stamps are uploaded to an S3 bucket, this Lambda function automatically:
- Extracts the date from the filename
- Creates a folder structure based on year/month/day
- Moves the file to the appropriate folder
- Cleans up the original file

This solves the common problem of S3's limitation in sorting objects when there are over 1,000 files.

## 🛠️ Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform 1.6.6 (managed via tfenv)
- Basic understanding of:
  - AWS services (Lambda, S3, IAM)
  - Python and boto3 SDK
  - Terraform

## 📁 Project Structure

```
aws-lambda-with-s3-trigger-terraform/
├── .gitignore
├── lambda.tf                 # Lambda and IAM resources
├── variables.tf              # Variable definitions
├── versions.tf               # Provider and backend configuration
├── lambda_functions/
│   └── main.py              # Lambda function code
├── pre-setup-script.sh      # Test script to generate sample files
├── setup.txt                # Environment setup instructions
└── readme.md                # This file
```

## 🚀 Setup Instructions

### 1. Install Prerequisites

```bash
# Install tfenv (Terraform version manager)
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install and use Terraform 1.6.6
tfenv install 1.6.6
tfenv use 1.6.6

# Verify installation
terraform --version
```

### 2. Configure AWS Credentials

```bash
# Configure AWS CLI
aws configure
```

Enter your AWS credentials when prompted:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name (e.g., ap-south-1)
- Default output format (e.g., json)

### 3. Create S3 Buckets

Create the following S3 buckets manually before deploying:

1. **Main bucket**: `inbound-bucket-custome`
   - Create a folder named `incoming/` inside this bucket

2. **Terraform state bucket**: `366140438193-terraform-state`

### 4. Deploy the Infrastructure

```bash
# Navigate to project directory
cd aws-lambda-with-s3-trigger-terraform

# Initialize Terraform
terraform init

# Review the deployment plan
terraform plan

# Deploy the infrastructure
terraform apply
```

Type `yes` when prompted to confirm the deployment.

## 🧪 Testing the Lambda Function

### Using the Test Script

Run the provided test script to generate sample files:

```bash
# Make the script executable
chmod +x pre-setup-script.sh

# Run the script
./pre-setup-script.sh
```

This script creates 10 files with the format `filename-[random]-YYYY-MM-DD.txt` and uploads them to the `incoming/` folder.

### Manual Testing

You can also test manually by uploading a file to the S3 bucket:

```bash
# Create a test file
echo "Test content" > test-file-2024-01-15.txt

# Upload to S3
aws s3 cp test-file-2024-01-15.txt s3://inbound-bucket-custome/incoming/
```

### Expected Behavior

After uploading files to `incoming/`:
1. Lambda function triggers automatically
2. Files are moved to organized folders: `incoming/YYYY/MM/DD/filename.txt`
3. Original files in `incoming/` are deleted

## 📝 Lambda Function Details

The Lambda function (`lambda_functions/main.py`):

1. Extracts bucket name and path from the `BUCKET_PATH` environment variable
2. Lists all files in the specified path
3. For each file:
   - Extracts year, month, and date from filename
   - Creates new path structure
   - Copies file to new location
   - Deletes original file

**Key Configuration:**
- Runtime: Python 3.11
- Timeout: 60 seconds
- Memory: 128 MB
- Trigger: S3 ObjectCreated events on `incoming/` prefix

## 🔧 Terraform Resources Created

1. **Lambda Function** (`aws_lambda_function.my_lambda_function`)
   - Executes the file organization logic

2. **IAM Role** (`aws_iam_role.lambda_role`)
   - Allows Lambda to assume role

3. **IAM Policy** (`aws_iam_policy.s3_bucket_policy`)
   - Grants permissions to read, write, and delete S3 objects

4. **S3 Bucket Notification** (`aws_s3_bucket_notification.lambda_trigger`)
   - Triggers Lambda on file uploads

5. **Lambda Permission** (`aws_lambda_permission.allow_s3_to_invoke_lambda`)
   - Allows S3 to invoke Lambda

6. **S3 Bucket Policy** (`aws_s3_bucket_policy.s3_bucket_policy`)
   - Allows Lambda to access bucket objects

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| BUCKET_PATH | S3 bucket and path for incoming files | inbound-bucket-custome/incoming/ |

### AWS Configuration

The project uses:
- Region: `ap-south-1` (Mumbai)
- Terraform state: Stored in S3 bucket `366140438193-terraform-state`

To modify these settings, edit `versions.tf`.

## 🧹 Cleanup

To remove all created resources:

```bash
terraform destroy
```

Type `yes` when prompted to confirm the destruction.

## 📋 Notes

- Never commit AWS credentials or sensitive information to version control
- The Lambda function processes files with date format: `filename-*-YYYY-MM-DD.txt`
- Ensure your AWS account has sufficient permissions to create the required resources
- Files are organized in the format: `incoming/YYYY/MM/DD/filename.txt`

## 🔍 Troubleshooting

1. **Lambda function not triggering**
   - Check S3 bucket notification configuration
   - Verify Lambda permissions
   - Ensure files are uploaded to the correct path (`incoming/`)

2. **Files not being moved**
   - Check Lambda function logs in CloudWatch
   - Verify IAM permissions
   - Ensure filename format matches expected pattern

3. **Terraform deployment errors**
   - Verify AWS credentials
   - Check if S3 buckets exist
   - Ensure Terraform version matches (1.6.6)

## 📚 Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html)

## 👤 Author

**Akhilesh Mishra**
- LinkedIn: [Akhilesh Mishra](https://www.linkedin.com/in/akhilesh-mishra-0ab886124/)
- Website: [Living DevOps](https://topmate.io/akhilesh_mishra/)

## 📄 License

This project is open source and available under the MIT License.
