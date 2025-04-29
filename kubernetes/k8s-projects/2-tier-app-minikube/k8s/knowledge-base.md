In Kubernetes, many but not all resources are namespace-scoped. Here are the main resources categorized by their namespace specificity:

Namespace-scoped resources:
* Pods
* Deployments
* Services
* Configmaps
* Secrets
* Jobs and CronJobs
* StatefulSets
* DaemonSets
* ReplicaSets
* PersistentVolumeClaims (PVCs)
* Roles and RoleBindings
* HorizontalPodAutoscalers (HPAs)
* Ingresses
* NetworkPolicies
* ResourceQuotas
* LimitRanges
* ServiceAccounts

Cluster-scoped resources (not namespace specific):
* Nodes
* PersistentVolumes (PVs)
* ClusterRoles and ClusterRoleBindings
* Namespaces themselves
* StorageClasses
* CustomResourceDefinitions (CRDs)
* ValidatingWebhookConfigurations
* MutatingWebhookConfigurations
* CertificateSigningRequests
* PodSecurityPolicies
* VolumeAttachments
* PriorityClasses
* RuntimeClasses

You can verify if a resource is namespaced by using the command:
```bash
kubectl api-resources --namespaced=true   # For namespace-scoped resources
kubectl api-resources --namespaced=false  # For cluster-scoped resources
```