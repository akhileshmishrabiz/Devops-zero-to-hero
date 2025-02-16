# EKS Cluster Infrastructure

This repository contains Terraform configurations for setting up an Amazon EKS cluster with associated resources.

## Infrastructure Components

### VPC Configuration
- Region: us-west-2
- CIDR Block: 10.0.0.0/16
- 3 Availability Zones
- Public and Private Subnets
- NAT Gateway for private subnet connectivity
- Internet Gateway for public access

### EKS Cluster
- Version: 1.29
- Private and Public endpoint access
- Cluster logging enabled for:
  - API server
  - Audit
  - Authenticator
  - Controller manager
  - Scheduler

### Node Groups
- Instance Type: t3.medium
- Min Size: 1
- Max Size: 3
- Desired Size: 2
- EBS Volume: 20GB gp3 (encrypted)
- Deployed in private subnets

## IAM Roles and Policies

### Cluster Role (eks-cluster-role)
Policies attached:
- AmazonEKSClusterPolicy
- AmazonEKSServicePolicy
- AmazonEKSVPCResourceController
- Custom Cluster Autoscaler Policy

### Node Group Role (eks-node-group-role)
Policies attached:
- AmazonEKSWorkerNodePolicy
- AmazonEKS_CNI_Policy
- AmazonEC2ContainerRegistryReadOnly
- AmazonSSMManagedInstanceCore
- Custom CloudWatch Logs Policy
- AWS Load Balancer Controller Policy

## Security Groups

### Cluster Security Group
- Inbound: Port 443 from worker nodes
- Outbound: All traffic allowed

### Node Security Group
- Inbound: All traffic from cluster security group
- Inbound: All traffic between nodes
- Outbound: All traffic allowed

## Using Private ECR Images in Kubernetes

### 1. Configure AWS CLI
```bash
aws configure
```

### 2. Update Kubeconfig
```bash
aws eks update-kubeconfig --region us-west-2 --name eks-cluster
```

### 3. Create ECR Repository (if not exists)
```bash
aws ecr create-repository --repository-name my-app --region us-west-2
```

### 4. Authenticate Docker with ECR
```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com
```

### 5. Tag and Push Image to ECR
```bash
docker tag my-app:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/my-app:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/my-app:latest
```

### 6. Create Kubernetes Secret for ECR
```bash
kubectl create secret docker-registry regcred \
  --docker-server=${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region us-west-2)
```

### 7. Create Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: ${AWS_ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/my-app:latest
      imagePullSecrets:
      - name: regcred
```

### 8. Apply the Deployment
```bash
kubectl apply -f deployment.yaml
```

## Terraform Commands

### Initialize Terraform
```bash
terraform init
```

### Plan Changes
```bash
terraform plan
```

### Apply Changes
```bash
terraform apply
```

### Destroy Infrastructure
```bash
terraform destroy
```

## Important Notes

1. **Cost Management**:
   - NAT Gateway and EKS cluster incur hourly charges
   - Consider destroying when not in use
   - Monitor EC2 instances in the node group

2. **Security**:
   - Cluster endpoint has public access enabled
   - Access is controlled via AWS IAM
   - Node groups are in private subnets
   - All EBS volumes are encrypted

3. **Maintenance**:
   - Regular updates to EKS version recommended
   - Monitor node group capacity
   - Check CloudWatch logs for issues

4. **Troubleshooting**:
   - Check node group status: `kubectl get nodes`
   - View pod logs: `kubectl logs <pod-name>`
   - Check cluster status: `aws eks describe-cluster --name eks-cluster`
   - View events: `kubectl get events --sort-by='.lastTimestamp'`