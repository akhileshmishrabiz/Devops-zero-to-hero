#### On github codespace ###
1. login to your github account 
2. in another tab open https://github.com/codespaces
3. go to "New codespace" , choose one of the repository in yout github account(create one repo if you dont have)
4. Choose 2/4 core machine and start. It will open a VScode lookalike. 
5. Open terminal, just like you do in your VScode
6. Install kubctl, minikube 

# install kubctl 
# https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.29.0/2024-01-04/bin/linux/amd64/kubectl


# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# start minikube cluster
minikube start
minikube status

# Run kubectl commands to check if its working 

# kubectl get pods , kubectl get pods -A
# kubectl get svc





########### On EC2 machine  #################
# Docs https://minikube.sigs.k8s.io/docs/start/

# take an ec2 with min 2 cpu, 20 gb of disk 

# Install docker
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# install kubctl 
# https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.29.0/2024-01-04/bin/linux/amd64/kubectl


# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# start minikube cluster
minikube start
minikube status


# kubectl get pods , kubectl get pods -A
# kubectl get svc