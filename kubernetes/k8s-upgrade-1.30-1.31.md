# Kubernetes Upgrade - Step by Step - 1.31 to 1.32

🚀 **A comprehensive guide for upgrading your Kubernetes cluster from 1.31 to 1.32**

## 1. Update Package Repository

Configure the repository for new K8s version:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
```

> Required when upgrading to a new minor version (e.g., 1.31-1.32)

## 2. Find Available Version

Find the latest 1.32.x version:

```bash
sudo apt update
sudo apt-cache madison kubeadm
```

> Determines the latest patch version available in repositories

## 3. Upgrade kubeadm First

Install new kubeadm version (replace x with patch version):

```bash
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.32.x-*' && \
sudo apt-mark hold kubeadm
```

> Upgrade the tool that orchestrates the upgrade process

## 4. Verify Upgrade Plan

Check upgrade feasibility and show component versions:

```bash
sudo kubeadm upgrade plan
```

> Validates cluster can be upgraded and shows upgrade path

## 5. Apply Upgrade (First Control Plane Only)

Execute the upgrade:

```bash
sudo kubeadm upgrade apply v1.32.x
```

> Updates control plane components and configurations

## 6. For Additional Nodes

Use "node" instead of "apply" command:

```bash
sudo kubeadm upgrade node
```

> Updates additional control planes without duplicate tasks

## 7. Drain Node Before kubelet Upgrade

Mark node unschedulable and evict workloads:

```bash
kubectl drain <node-name> --ignore-daemonsets
```

> Ensures workloads don't get disrupted during kubelet restart

## 8. Upgrade kubelet and kubectl

Install new kubelet and kubectl:

```bash
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='1.32.x-*' kubectl='1.32.x-*' && \
sudo apt-mark hold kubelet kubectl
```

> Upgrades node-level Kubernetes components

## 9. Restart kubelet Service

Apply changes and restart kubelet:

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

> Applies new configuration and starts new kubelet version

## 10. Uncordon Node

Make node schedulable again:

```bash
kubectl uncordon <node-name>
```

> Returns node to active service after successful upgrade

## 11. Verify Cluster Status

Confirm all nodes ready and upgraded:

```bash
kubectl get nodes
```

> Validates successful upgrade of all nodes

---

Created by @DeleLeansTech
