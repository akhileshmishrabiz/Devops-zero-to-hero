# Kubernetes Questions and Answers Guide

## 1. Pod Scheduling Across Nodes

**Q: In a cluster with two nodes, one with pods and the other without, which node will a new pod be scheduled to?**

The scheduling outcome depends on several factors and configurations, including:

- Pod affinity settings
- Taints and tolerations
- Scheduling plugins

With default configurations and equal resource availability, the NodeResourcesFit plugin's scoring strategy determines placement:

- LeastAllocated (default): Prioritizes nodes with lowest resource usage, favoring empty nodes
- MostAllocated: Prefers nodes with higher resource usage, favoring nodes with existing pods
- RequestedToCapacityRatio: Balances resource utilization across nodes

## 2. Container OOM Behavior

**Q: If an application running in a container encounters an OOM (Out-of-Memory) error, will the container restart, or will the entire Pod be recreated?**

When an OOM error occurs:

- The container typically restarts based on the Pod's RestartPolicy (defaults to Always)
- The Pod itself remains intact and is not recreated
- In extreme cases with severe node memory pressure, the Pod might be evicted, leading to recreation

## 3. Dynamic Configuration Updates

**Q: Can application configurations such as environment variables or ConfigMap updates be applied dynamically without recreating the Pod?**

Configuration update behavior varies:

- Environment variables cannot be updated dynamically
- ConfigMap updates can be applied dynamically if:
  - Mounted as files
  - Not using subPath
- Update synchronization depends on:
  - kubelet's syncFrequency (default: 1 minute)
  - configMapAndSecretChangeDetectionStrategy settings

## 4. Pod Stability

**Q: Is a Pod stable once created, even if the user takes no further action?**

Pod stability is not guaranteed. Various factors can lead to Pod eviction:

- Resource shortages
- Network disruptions
- Node failures
- System maintenance

## 5. ClusterIP Service Load Balancing

**Q: Can a Service of type ClusterIP ensure load balancing for TCP traffic?**

ClusterIP Services handle TCP traffic with some limitations:

- Uses Linux kernel Netfilter for load balancing
- Connection tracking maintains session persistence
- Long-lived TCP connections may result in uneven load distribution
- Better suited for short-lived connections

## 6. Application Log Collection

**Q: How should application logs be collected, and is there a risk of losing logs?**

Logging approaches and considerations:

- Standard output (stdout/stderr):
  - Saved on the node
  - Collected via log agents (Fluentd, Filebeat) as DaemonSet
  - Risk of loss if Pod is deleted before collection
- File-based logging:
  - Written to persistent storage
  - Prevents log loss
  - Requires storage configuration

## 7. Liveness Probe Reliability

**Q: If an HTTP Server Pod's livenessProbe is functioning correctly, does it mean the application is problem-free?**

Liveness probe limitations:

- Application perspective:
  - Only checks if application is alive
  - Doesn't verify correct functionality
  - Application can be degraded while passing probe
- Network perspective:
  - Checks requests from node's kubelet
  - Doesn't guarantee cross-node network reliability

## 8. Application Scaling

**Q: How can an application scale to handle traffic fluctuations?**

Kubernetes provides multiple scaling options:

- Horizontal Pod Autoscaling (HPA):
  - Most commonly used
  - Dynamically adjusts Pod count
  - Based on metrics (CPU, request rate, custom metrics)
- Vertical Pod Autoscaling (VPA):
  - Adjusts Pod resources
  - Requires Pod recreation
  - Limited use cases
- External scaling:
  - Through kube-apiserver requests
  - Custom metrics-based scaling

## 9. kubectl exec Understanding

**Q: When you execute kubectl exec -it <pod> -- bash, are you logging into the pod?**

No, the command behavior is more specific:

- Targets a specific container (defaults to single container in Pod)
- Pods are collections of isolated Linux namespaces
- Containers share Network, IPC, and UTS namespaces
- PID and Mount namespaces remain separate
- Creates new bash process in container's isolated environment

## 10. Troubleshooting Container Restarts

**Q: How would you troubleshoot if a container in a Pod repeatedly exits and restarts?**

Troubleshooting approach:

- kubectl exec won't work with crashing containers
- Investigation methods:
  - Examine node logs
  - Review container logs
  - Check Pod status
  - Use kubectl debug to start temporary container
  - Investigate environment and dependencies
