Prerequisites:
1. Install aws cli and configure creds

   
3. Install kubectl

   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.30.2/2024-07-12/bin/linux/amd64/kubectl
   
  sha256sum -c kubectl.sha256

openssl sha1 -sha256 kubectl

chmod +x ./kubectl

mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH

echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc


5. install eksctl cli

   # Replace amd64 with armv6, armv7 or arm64
 (Get-FileHash -Algorithm SHA256 .\eksctl_Windows_amd64.zip).Hash -eq ((Get-Content .\eksctl_checksums.txt) -match 'eksctl_Windows_amd64.zip' -split ' ')[0]
 ```

#### Using Git Bash: 
```sh
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=windows_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.zip"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

unzip eksctl_$PLATFORM.zip -d $HOME/bin

rm eksctl_$PLATFORM.zip
4. Check if creds are configured
   aws sts get-caller-identity

5. Create cluster
eksctl create cluster --name my-cluster --region region-code

or use Fargate
eksctl create cluster --name my-cluster --region region-code --fargate
```

##### Connect to cluser from a VM (ec2)    #######
```sh
# install kubectl
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.31.0/2024-09-12/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo cp ./kubectl /usr/local/bin
export PATH=/usr/local/bin:$PATH
kubectl version --client=true

# install aws cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version

# attach a iam profile for access to eks

# get cluster info
EKS_CLUSTER_NAME=$(aws eks list-clusters --region us-west-2 --query clusters[0] --output text)
echo $EKS_CLUSTER_NAME

aws eks update-kubeconfig --name $EKS_CLUSTER_NAME --region us-west-2
cat ~/.kube/config

# run kubectl commands
kubectl get nodes 
kubectl describe nodes

```
##### Install helm ######
``` sh
{
curl -sLO https://get.helm.sh/helm-v3.7.1-linux-amd64.tar.gz
tar -xvf helm-v3.7.1-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin
}

{
mkdir -p ~/cloudacademy/observability
cd ~/cloudacademy/observability
curl -sL https://api.github.com/repos/cloudacademy/k8s-lab-observability1/releases/latest | \
 jq -r '.zipball_url' | \
 wget -qi -
unzip release* && find -type f -name *.sh -exec chmod +x {} \;
cd cloudacademy-k8s-lab-observability*
tree
}

kubectl create ns cloudacademy
cd ./code/k8s && ls -la
kubectl apply -f ./api.yaml

kubectl run api-client \
 --namespace=cloudacademy \
 --image=cloudacademydevops/api-generator \
 --env="API_URL=http://api-service:5000" \
 --image-pull-policy IfNotPresent

{
kubectl wait --for=condition=available --timeout=300s deployment/api -n cloudacademy
kubectl wait --for=condition=ready --timeout=300s pod/api-client -n cloudacademy
}


# install helm

kubectl create ns prometheus

cd ../prometheus && ls -la
sed -i 's/extraEnv: {}/extraEnv:/g' prometheus.values.yaml

{
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus \
 --namespace prometheus \
 --set alertmanager.persistentVolume.storageClass="gp2" \
 --set server.persistentVolume.storageClass="gp2" \
 --values ./prometheus.values.yaml
}


kubectl expose deployment prometheus-server \
 --namespace prometheus \
 --name=prometheus-server-loadbalancer \
 --type=LoadBalancer \
 --port=80 \
 --target-port=9090

{
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-kube-state-metrics -n prometheus
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-prometheus-pushgateway -n prometheus
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-server -n prometheus
}

kubectl get all -n prometheus

{
PROMETHEUS_ELB_FQDN=$(kubectl get svc -n prometheus prometheus-server-loadbalancer -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
until nslookup $PROMETHEUS_ELB_FQDN >/dev/null 2>&1; do sleep 2 && echo waiting for DNS to propagate...; done
curl -sD - -o /dev/null $PROMETHEUS_ELB_FQDN/graph
}

# Note: DNS propagation can take up to 2-5 minutes, please be patient while the propagation proceeds - it will eventually complete.

echo http://$PROMETHEUS_ELB_FQDN
# access the DNS name to access the Prometheus server

## Install Grafana

cd ../grafana && ls -la

kubectl create ns grafana

{
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana grafana/grafana \
 --namespace grafana \
 --set persistence.storageClassName="gp2" \
 --set persistence.enabled=true \
 --set adminPassword="EKS:l3t5g0" \
 --set service.type=LoadBalancer \
 --values ./grafana.values.yaml
}

kubectl wait --for=condition=available --timeout=300s deployment/grafana -n grafana 

kubectl get all -n grafana

# Confirm that the Grafana ELB FQDN has propagated and resolves. In the terminal run the following commands:

{
GRAFANA_ELB_FQDN=$(kubectl get svc -n grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
until nslookup $GRAFANA_ELB_FQDN >/dev/null 2>&1; do sleep 2 && echo waiting for DNS to propagate...; done
curl -I $GRAFANA_ELB_FQDN/login
}

echo http://$GRAFANA_ELB_FQDN

# Email or username: admin

# Password: EKS:l3t5g0  (or you can get the value from secret)

```
Import the dashboard 3119 and see how it looks.

now use the 

 Open a new browser tab and navigate to the following sample API monitoring dashboard URL:

https://raw.githubusercontent.com/cloudacademy/k8s-lab-observability1/main/code/grafana/dashboard.json
, opens in a new tab

Note: The same dashboard.json file is located in the project directory (./code/grafana/dashboard.json) and can be copied directly from there if easier.
   
