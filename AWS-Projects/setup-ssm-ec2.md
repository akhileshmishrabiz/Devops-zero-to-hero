Setting up SSM (AWS Systems Manager) to log in to EC2 instances without public IPs is a great way to improve security and simplify access management. Here's how to do it:

## Prerequisites
1. An AWS account with appropriate permissions
2. EC2 instance(s) in a VPC
3. AWS CLI installed and configured on your local machine

## Step-by-Step Guide

### 1. Create an IAM Role for EC2 with SSM permissions
1. Go to IAM console
2. Create a new role for EC2
3. Attach the `AmazonSSMManagedInstanceCore` policy
4. (Optional) Add additional policies if needed
5. Name the role (e.g., "EC2SSMRole") and create it

### 2. Ensure your EC2 instance has the SSM agent installed
- Most recent Amazon Linux, Ubuntu, and Windows AMIs come with the SSM agent pre-installed
- For other distributions, you may need to install it manually

### 3. Attach the IAM role to your EC2 instance
1. Go to EC2 console
2. Select your instance
3. Actions → Security → Modify IAM role
4. Select the role you created earlier
5. Save

### 4. Set up network requirements
1. Ensure your VPC has a VPC endpoint for SSM:
   ```
   aws ec2 create-vpc-endpoint --vpc-id your-vpc-id --service-name com.amazonaws.your-region.ssm --vpc-endpoint-type Interface
   ```
2. Create endpoints for ec2messages and ssmmessages as well:
   ```
   aws ec2 create-vpc-endpoint --vpc-id your-vpc-id --service-name com.amazonaws.your-region.ec2messages --vpc-endpoint-type Interface
   aws ec2 create-vpc-endpoint --vpc-id your-vpc-id --service-name com.amazonaws.your-region.ssmmessages --vpc-endpoint-type Interface
   ```
3. Ensure your security groups allow outbound HTTPS traffic (port 443)

### 5. Connect to your instance using the AWS CLI
```bash
aws ssm start-session --target i-0123456789abcdef0
```

### 6. To use SSH through SSM (for a more familiar interface)
1. Install the Session Manager plugin for the AWS CLI
2. Add this to your SSH config (~/.ssh/config):
   ```
   host i-* mi-*
     ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
   ```
3. Connect via SSH:
   ```bash
   ssh -i your-key-pair.pem ec2-user@i-0123456789abcdef0
   ```

### 7. Bonus: Set up port forwarding for other applications if needed
```bash
aws ssm start-session --target i-0123456789abcdef0 --document-name AWS-StartPortForwardingSession --parameters '{"portNumber":["3306"],"localPortNumber":["3306"]}'
```

This setup eliminates the need for bastion hosts, public IPs, and open SSH ports, making your infrastructure more secure while simplifying access management.
