
```markdown
# Prerequisites

## 1. Install AWS CLI and Configure Credentials
Ensure that you have AWS CLI installed and your credentials configured.

```sh
aws configure
```

## 2. Install kubectl
```sh
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.30.2/2024-07-12/bin/linux/amd64/kubectl
sha256sum -c kubectl.sha256
openssl sha1 -sha256 kubectl
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
```

## 3. Install eksctl CLI

### Windows (PowerShell)
```powershell
# Replace amd64 with armv6, armv7, or arm64
(Get-FileHash -Algorithm SHA256 .\eksctl_Windows_amd64.zip).Hash -eq ((Get-Content .\eksctl_checksums.txt) -match 'eksctl_Windows_amd64.zip' -split ' ')[0]
```

### Using Git Bash
```sh
# For ARM systems, set ARCH to: `arm64`, `armv6`, or `armv7`
ARCH=amd64
PLATFORM=windows_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.zip"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

unzip eksctl_$PLATFORM.zip -d $HOME/bin
rm eksctl_$PLATFORM.zip
```
or use the link

https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

## 4. Verify AWS Credentials
```sh
aws sts get-caller-identity
```

## 5. Create an EKS Cluster
```sh
eksctl create cluster --name my-cluster --region <region-code>
```
or use Fargate:
```sh
eksctl create cluster --name my-cluster --region <region-code> --fargate
```

---

## Connect to the Cluster from a VM (EC2)
```sh
# Install kubectl
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.31.0/2024-09-12/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo cp ./kubectl /usr/local/bin
export PATH=/usr/local/bin:$PATH
kubectl version --client=true
```

```sh
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

```sh
# Attach an IAM profile for access to EKS

# Get cluster info
EKS_CLUSTER_NAME=$(aws eks list-clusters --region us-west-2 --query clusters[0] --output text)
echo $EKS_CLUSTER_NAME

aws eks update-kubeconfig --name $EKS_CLUSTER_NAME --region us-west-2
cat ~/.kube/config
```

```sh
# Run kubectl commands
kubectl get nodes 
kubectl describe nodes
```

---

## Install Helm
```sh
curl -sLO https://get.helm.sh/helm-v3.7.1-linux-amd64.tar.gz
tar -xvf helm-v3.7.1-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin
```

---

## Deploy Observability Stack
```sh
mkdir -p ~/cloudacademy/observability
cd ~/cloudacademy/observability
curl -sL https://api.github.com/repos/cloudacademy/k8s-lab-observability1/releases/latest | \
 jq -r '.zipball_url' | \
 wget -qi -
unzip release* && find -type f -name *.sh -exec chmod +x {} \;
cd cloudacademy-k8s-lab-observability*
tree
```

```sh
kubectl create ns cloudacademy
cd ./code/k8s && ls -la
kubectl apply -f ./api.yaml
```

```sh
kubectl run api-client \
 --namespace=cloudacademy \
 --image=cloudacademydevops/api-generator \
 --env="API_URL=http://api-service:5000" \
 --image-pull-policy IfNotPresent
```

```sh
kubectl wait --for=condition=available --timeout=300s deployment/api -n cloudacademy
kubectl wait --for=condition=ready --timeout=300s pod/api-client -n cloudacademy
```

---

## Install Prometheus with Helm
```sh
kubectl create ns prometheus
cd ../prometheus && ls -la
sed -i 's/extraEnv: {}/extraEnv:/g' prometheus.values.yaml
```

```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus \
 --namespace prometheus \
 --set alertmanager.persistentVolume.storageClass="gp2" \
 --set server.persistentVolume.storageClass="gp2" \
 --values ./prometheus.values.yaml
```

```sh
kubectl expose deployment prometheus-server \
 --namespace prometheus \
 --name=prometheus-server-loadbalancer \
 --type=LoadBalancer \
 --port=80 \
 --target-port=9090
```

```sh
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-kube-state-metrics -n prometheus
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-prometheus-pushgateway -n prometheus
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-server -n prometheus
```

```sh
kubectl get all -n prometheus
```

```sh
PROMETHEUS_ELB_FQDN=$(kubectl get svc -n prometheus prometheus-server-loadbalancer -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
until nslookup $PROMETHEUS_ELB_FQDN >/dev/null 2>&1; do sleep 2 && echo waiting for DNS to propagate...; done
curl -sD - -o /dev/null $PROMETHEUS_ELB_FQDN/graph
```

```sh
echo http://$PROMETHEUS_ELB_FQDN
```
---

## Install Grafana
```sh
cd ../grafana && ls -la
kubectl create ns grafana
```

```sh
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana grafana/grafana \
 --namespace grafana \
 --set persistence.storageClassName="gp2" \
 --set persistence.enabled=true \
 --set adminPassword="EKS:l3t5g0" \
 --set service.type=LoadBalancer \
 --values ./grafana.values.yaml
```

```sh
kubectl wait --for=condition=available --timeout=300s deployment/grafana -n grafana 
kubectl get all -n grafana
```

```sh
GRAFANA_ELB_FQDN=$(kubectl get svc -n grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
until nslookup $GRAFANA_ELB_FQDN >/dev/null 2>&1; do sleep 2 && echo waiting for DNS to propagate...; done
curl -I $GRAFANA_ELB_FQDN/login
```

```sh
echo http://$GRAFANA_ELB_FQDN
```

**Grafana Login:**
- **Username:** `admin`
- **Password:** `EKS:l3t5g0` (or retrieve from secret)

---

## Import the Dashboard
Import **dashboard ID: 3119** in Grafana for monitoring.

You can also use the following URL:
```
https://raw.githubusercontent.com/cloudacademy/k8s-lab-observability1/main/code/grafana/dashboard.json
```

---

