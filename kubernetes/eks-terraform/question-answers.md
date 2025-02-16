EKS FAQ - Questions and Answers
===============================

Q1: How can I use AWS IAM permissions for ECR image pull instead of Kubernetes secrets with token?
------------------------------------------------------------------------------------------------

A: To use AWS IAM permissions for ECR image pull, you need to:

1. Create an IAM role for service account (IRSA):
```bash
# Create IAM OIDC provider for your cluster
eksctl utils associate-iam-oidc-provider \
    --cluster eks-cluster \
    --approve
```

2. Create IAM Policy for ECR access:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability"
            ],
            "Resource": "arn:aws:ecr:region:account-id:repository/repo-name"
        }
    ]
}
```

3. Create an IAM role and attach the policy:
```bash
# Create service account and IAM role
eksctl create iamserviceaccount \
    --name ecr-access-sa \
    --namespace default \
    --cluster eks-cluster \
    --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/ecr-access-policy \
    --approve
```

4. Use the service account in your deployment:
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
      serviceAccountName: ecr-access-sa  # Specify the service account
      containers:
      - name: my-app
        image: ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/my-app:latest
```

Benefits of this approach:
- No need to manage Kubernetes secrets
- No token expiration issues
- More secure as it uses AWS IAM roles
- Follows AWS security best practices
- Easier to manage permissions through AWS IAM

Note: Make sure your EKS cluster has OIDC provider configured. You can verify with:
```bash
aws eks describe-cluster --name eks-cluster --query "cluster.identity.oidc.issuer" --output text
```

Q: What are the best practices for implementing microservices with egress in EKS, and how to handle domain/subdomain mapping and inter-service communication?

A: The implementation can be broken down into three main components:

1. Egress Control Configuration:
- Use AWS VPC CNI and Calico for network policies
- Configure egress policies per microservice namespace:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-specific-egress
  namespace: service-a
spec:
  podSelector:
    matchLabels:
      app: service-a
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: service-b
    ports:
    - protocol: TCP
      port: 8080
```

2. Domain/Subdomain Mapping:
- Use AWS ALB Ingress Controller for subdomain routing
- Configure Route53 for DNS management
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: microservices-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS-1-2-2017-01
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:region:account:certificate/cert-id
spec:
  rules:
  - host: service-a.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: service-a
            port:
              number: 80
  - host: service-b.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: service-b
            port:
              number: 80
```

3. Inter-Service Communication:

a. Service-to-Service Direct Communication:
- Use Kubernetes Service DNS:
  - Within same namespace: `service-b.svc.cluster.local`
  - Cross namespace: `service-b.namespace-b.svc.cluster.local`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-b
  namespace: namespace-b
spec:
  selector:
    app: service-b
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

b. Cross-Namespace Access Control:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-cross-namespace
  namespace: namespace-b
spec:
  podSelector:
    matchLabels:
      app: service-b
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: namespace-a
    ports:
    - protocol: TCP
      port: 8080
```

Best Practices:

1. Security:
   - Implement mTLS between services
   - Use namespace isolation
   - Enable network policies by default
   - Use IAM roles for service accounts (IRSA)

2. Networking:
   - Always use specific egress rules
   - Implement proper health checks
   - Use service mesh for complex routing
   - Enable access logging on ALB

3. Monitoring:
   - Implement distributed tracing
   - Set up centralized logging
   - Use Prometheus for metrics
   - Monitor inter-service latency

4. Performance:
   - Use connection pooling
   - Implement circuit breakers
   - Enable horizontal pod autoscaling
   - Use proper resource limits

Setup Steps:

1. Configure DNS and SSL:
```bash
# Create SSL certificate in ACM
aws acm request-certificate \
  --domain-name "*.example.com" \
  --validation-method DNS

# Configure Route53
aws route53 create-hosted-zone \
  --name example.com \
  --caller-reference $(date +%s)
```

2. Install ALB Ingress Controller:
```bash
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --namespace kube-system \
  --set clusterName=cluster-name \
  --set serviceAccount.create=true
```

3. Enable Network Policies:
```bash
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/master/calico-operator.yaml
```

This setup provides:
- Secure inter-service communication
- Proper domain/subdomain routing
- Controlled egress access
- Scalable microservices architecture