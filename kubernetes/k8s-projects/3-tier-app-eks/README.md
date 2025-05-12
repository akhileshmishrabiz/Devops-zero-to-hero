# Production-Ready 3-Tier Application on AWS EKS

This project demonstrates the deployment of a production-ready 3-tier application on Amazon Elastic Kubernetes Service (EKS). The architecture comprises:

* **Frontend**: React application
* **Backend**: Flask API
* **Database**: PostgreSQL hosted on Amazon RDS([meduim](https://towardsaws.com/stop-following-useless-tutorials-learn-kubernetes-on-aws-like-a-pro-1186aa8a33ac))

The setup includes Kubernetes manifests for deploying the application components, configuring services, secrets, config maps, ingress, and integrating with AWS resources like RDS and Route 53.

---

## Prerequisites

Ensure you have the following installed and configured:

* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
* [eksctl](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [Helm](https://helm.sh/docs/intro/install/)
* An AWS account with appropriate permissions([LinkedIn][2], [livingdevops.com][3], [Medium][4])

---

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/kubernetes-zero-to-hero.git
cd kubernetes-zero-to-hero/3-tier-app-eks/k8s
```



### 2. Create EKS Cluster

```bash
eksctl create cluster \
  --name Akhilesh-cluster \
  --region eu-west-1 \
  --version 1.31 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```



This command sets up an EKS cluster with a managed node group.([LinkedIn][2])

### 3. Configure kubectl

```bash
aws eks --region eu-west-1 update-kubeconfig --name Akhilesh-cluster
```



### 4. Create Kubernetes Namespace

```bash
kubectl apply -f namespace.yaml
```



### 5. Deploy RDS PostgreSQL Instance

Set up a PostgreSQL instance on Amazon RDS. Once created, note the following details:

* **DB\_HOST**: RDS endpoint
* **DB\_NAME**: postgres
* **DB\_USERNAME**: postgresadmin
* **DB\_PASSWORD**: YourStrongPassword123!([livingdevops.com][3])

### 6. Create ExternalName Service for RDS

Update `database-service.yaml` with your RDS endpoint:([livingdevops.com][3])

```yaml
externalName: your-rds-endpoint.rds.amazonaws.com
```



Apply the service:

```bash
kubectl apply -f database-service.yaml
```



### 7. Create Secrets and ConfigMaps

Encode your credentials in base64:([livingdevops.com][3])

```bash
echo -n 'postgresadmin' | base64
echo -n 'YourStrongPassword123!' | base64
echo -n 'postgresql://postgresadmin:YourStrongPassword123!@postgres-db.3-tier-app-eks.svc.cluster.local:5432/postgres' | base64
```



Update `secrets.yaml` and `configmap.yaml` with the encoded values, then apply:([livingdevops.com][3])

```bash
kubectl apply -f secrets.yaml
kubectl apply -f configmap.yaml
```



### 8. Run Database Migrations

```bash
kubectl apply -f migration_job.yaml
```



Monitor the job:

```bash
kubectl get jobs -n 3-tier-app-eks
kubectl logs job/database-migration -n 3-tier-app-eks
```



### 9. Deploy Backend and Frontend

```bash
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
```



Check deployments:

```bash
kubectl get deployments -n 3-tier-app-eks
kubectl get services -n 3-tier-app-eks
```



### 10. Access the Application

Port-forward the services:([livingdevops.com][3])

```bash
# Backend
kubectl port-forward svc/backend 8000:8000 -n 3-tier-app-eks

# Frontend
kubectl port-forward svc/frontend 8080:80 -n 3-tier-app-eks
```



Access the application:([livingdevops.com][3])

* Backend API: `http://localhost:8000/api/topics`
* Frontend UI: `http://localhost:8080`([livingdevops.com][3])

### 11. Configure Ingress with AWS ALB

Apply the ingress resources:

```bash
kubectl apply -f ingress.yaml
```



Verify ingress:

```bash
kubectl get ingress -n 3-tier-app-eks
```



Ensure your subnets are tagged appropriately for the AWS Load Balancer Controller to create an ALB.([livingdevops.com][3])

### 12. Set Up Domain with Route 53

Create a hosted zone for your domain:([livingdevops.com][3])

```bash
aws route53 create-hosted-zone --name yourdomain.com --caller-reference $(date +%s)
```



Update your domain's name servers with the ones provided by Route 53.

Create an alias record pointing to the ALB DNS:([livingdevops.com][3])

```bash
# Get ALB DNS
ALB_DNS=$(kubectl get ingress 3-tier-app-ingress -n 3-tier-app-eks -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Get Hosted Zone ID
ZONE_ID=$(aws route53 list-hosted-zones-by-name --dns-name yourdomain.com --query "HostedZones[0].Id" --output text | sed 's/\/hostedzone\///')

# Create alias record
aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID --change-batch '{
  "Comment": "Creating alias record for ALB",
  "Changes": [{
    "Action": "CREATE",
    "ResourceRecordSet": {
      "Name": "app.yourdomain.com",
      "Type": "A",
      "AliasTarget": {
        "HostedZoneId": "Z32O12XQLNTSW2",
        "DNSName": "'$ALB_DNS'",
        "EvaluateTargetHealth": false
      }
    }
  }]
}'
```



---

## Application Overview

This application is a DevOps-themed quiz platform. The backend API provides endpoints to manage quiz topics and questions, while the frontend offers an interactive UI for users to participate in quizzes.

Sample CSV files for bulk question uploads are available in the `backend/questions-answers` directory.([livingdevops.com][3])

---

## Troubleshooting

* **Database Connectivity**: Ensure the security group associated with the RDS instance allows inbound traffic from the EKS cluster's security group on port 5432.
* **Ingress Issues**: Verify that your subnets are tagged correctly for the AWS Load Balancer Controller to function.
* **Logs**: Check pod logs for debugging:([livingdevops.com][3])

```bash
kubectl logs -n 3-tier-app-eks -l app=backend
kubectl logs -n 3-tier-app-eks -l app=frontend
```



---

## License

This project is licensed under the MIT License.

---

For a detailed walkthrough and explanations, refer to the original blog post: [How To Deploy A Production-Ready 3-Tier Application On AWS EKS With Real-World Setup](https://livingdevops.com/devops/deploying-a-production-ready-3-tier-app-on-aws-eks-with-eks/)([livingdevops.com][5])

---

[1]: https://medium.com/%40silas.cloudspace/containerizing-and-deploying-a-three-tier-application-on-aws-eks-with-kubernetes-bd9b0eaf2648?utm_source=chatgpt.com "Containerizing and Deploying a Three-Tier Application on AWS EKS ..."
[2]: https://www.linkedin.com/pulse/how-i-deployed-3-tier-web-app-aws-eks-using-kubernetes-usama-malik-yeiec?utm_source=chatgpt.com "How I Deployed a 3-Tier Web App on AWS EKS Using Kubernetes"
[3]: https://livingdevops.com/devops/deploying-a-production-ready-3-tier-app-on-aws-eks-with-eks/?utm_source=chatgpt.com "How To Deploy A Production-Ready 3-Tier Application On AWS ..."
[4]: https://jay75chauhan.medium.com/streamlined-end-to-end-devsecops-kubernetes-three-tier-project-with-aws-eks-terraform-argocd-0ab73d9de11f?utm_source=chatgpt.com "Streamlined End-to-End DevSecOps Kubernetes Three-Tier Project ..."
[5]: https://livingdevops.com/category/devops/?utm_source=chatgpt.com "Category Devops"
