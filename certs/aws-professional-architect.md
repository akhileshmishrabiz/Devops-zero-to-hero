# AWS Solutions Architect Professional Exam Overview

The exam tests your ability to:
- Design and deploy dynamically scalable, highly available, fault-tolerant, and reliable applications
- Implement cost-control strategies
- Design appropriate migration of applications and data
- Select appropriate AWS services to design complex cloud architectures

Let's cover the main domains you need to study:

## 1. Design for Organizational Complexity

### Multi-Account Management
- AWS Organizations
- Service Control Policies (SCPs)
- AWS Control Tower
- Cross-account roles and access

### Network Design
- VPC design patterns (multi-VPC architectures)
- Transit Gateway vs VPC Peering
- VPC Endpoints and PrivateLink
- Hybrid connectivity (Direct Connect, VPN)

### Authentication and Authorization
- IAM policies and roles
- AWS SSO/IAM Identity Center
- Resource-based policies
- Cross-account access

## 2. Design for New Solutions

### Compute Solutions
- EC2 instance types and placement groups
- Container services (ECS, EKS)
- Serverless computing (Lambda, Fargate)
- Auto Scaling strategies

### Storage Solutions
- S3 storage classes and lifecycle policies
- EBS volume types
- EFS vs FSx
- Storage Gateway options

### Database Solutions
- RDS (multi-AZ, read replicas)
- DynamoDB (capacity planning, DAX)
- ElastiCache
- Aurora (Global Database, Serverless)
- Database migration strategies

### Serverless Architectures
- API Gateway
- Step Functions
- EventBridge
- SQS, SNS, and Kinesis

## 3. Migration Planning

### Migration Strategies (6 Rs)
- Rehost, Replatform, Repurchase
- Refactor, Retain, Retire

### AWS Migration Tools
- Application Discovery Service
- Database Migration Service (DMS)
- Server Migration Service (SMS)
- CloudEndure Migration

### Data Transfer Options
- Snowball, Snowmobile
- DataSync
- Transfer acceleration

## 4. Cost Control

### Cost Optimization Strategies
- Reserved Instances vs Savings Plans
- Spot Instances
- Right-sizing resources
- AWS Cost Explorer and Budgets

### Resource Tagging and Allocation
- Cost allocation tags
- Resource Groups
- AWS Organizations for billing

## 5. Continuous Improvement

### Monitoring and Observability
- CloudWatch metrics and logs
- CloudTrail
- X-Ray

### High Availability and Disaster Recovery
- Multi-AZ vs Multi-Region
- Backup strategies
- Route 53 routing policies
- Recovery time objective (RTO) and recovery point objective (RPO)

### Security and Compliance
- AWS Config and AWS Security Hub
- GuardDuty and Macie
- KMS and CloudHSM
- WAF, Shield, and Firewall Manager
- Security compliance frameworks (PCI DSS, HIPAA, etc.)

## 6. Key Design Patterns

### Microservices Architecture
- Service-oriented design
- API-driven development
- Container orchestration

### Event-Driven Architecture
- Pub/sub patterns
- Decoupled systems
- Real-time processing

### Caching Strategies
- CloudFront
- ElastiCache
- DAX

### Resilience Patterns
- Circuit breakers
- Bulkheads
- Retries and backoff strategies

## Study Resources

1. AWS Official Documentation
2. AWS Whitepapers, especially:
   - AWS Well-Architected Framework
   - Security Best Practices
   - Serverless Applications Lens
   - Disaster Recovery approaches
3. Hands-on Labs through AWS Free Tier
4. Official AWS practice exams
