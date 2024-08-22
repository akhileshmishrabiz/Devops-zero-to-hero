In this project, I will be using Terraform to provision an EC2 bastion host, a private EC2 instance, S3 buckets, and an IAM role to access S3 buckets. 
I will also show you how we can use the VPC gateway endpoint to access S3 without going to the Internet.

**Blog post explaining everything**
https://medium.com/@akhilesh-mishra/devops-zero-to-hero-2-access-s3-bucket-from-ec2-instances-with-private-and-public-endpoints-94fb35133cf8

AWS services used:

Ec2, IAM, S3, VPC, VPC gateway endpoints.

Terraform concepts:

provisioners, data source, output, explict and implict dependencies, string interpolations
