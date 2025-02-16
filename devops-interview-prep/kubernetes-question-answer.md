# Kubernetes Questions and Answers

1. **In a cluster with two nodes, one with pods and the other without, which node will a new pod be scheduled to?**

The result depends on configurations such as Pod affinity, taints and tolerations, and scheduling plugins. However, assuming default configurations and equal resource availability on both nodes, the NodeResourcesFit plugin plays a critical role. Its scoring strategies include LeastAllocated (default, prioritizing nodes with the least resource usage), MostAllocated (prioritizing nodes with higher resource usage), and RequestedToCapacityRatio (balancing resource utilization). Using the MostAllocated strategy, new pods would be scheduled to nodes with existing pods, whereas the other two strategies would prefer empty nodes.

2. **If an application running in a container encounters an OOM (Out-of-Memory) error, will the container restart, or will the entire Pod be recreated?**

When a container runs out of memory, it typically restarts based on the Pod's RestartPolicy (default is Always). The Pod itself remains intact. However, under extreme conditions, such as severe memory pressure on the node, the Pod might be evicted, resulting in its recreation.

3. **Can application configurations such as environment variables or ConfigMap updates be applied dynamically without recreating the Pod?**

Environment variables cannot be updated dynamically. However, ConfigMap updates can be applied dynamically if mounted as files (not using subPath). Synchronization delay depends on kubelet's syncFrequency (default 1 minute) and configMapAndSecretChangeDetectionStrategy.

4. **Is a Pod stable once created, even if the user takes no further action?**

A Pod is not guaranteed to remain stable. Factors like resource shortages or network disruptions could lead to Pod eviction, even without user intervention.

5. **Can a Service of type ClusterIP ensure load balancing for TCP traffic?**

ClusterIP-based Services rely on Linux kernel Netfilter for load balancing. Its connection tracking mechanism maintains session persistence for established TCP connections. This can result in uneven load distribution for long-lived connections.

6. **How should application logs be collected, and is there a risk of losing logs?**

Logs can be output to stdout/stderr or written to files. For stdout/stderr, logs are saved on the node and can be collected using log agents like Fluentd or Filebeat (typically deployed as DaemonSet). However, if a Pod is deleted, its logs may be lost before the agent collects them. Writing logs to files on persistent storage can prevent loss.

7. **If an HTTP Server Pod's livenessProbe is functioning correctly, does it mean the application is problem-free?**

From an application perspective, livenessProbe only checks if the application is alive, not whether it functions correctly. The application might be in a degraded state while still passing the probe. From a network perspective, livenessProbe (e.g., httpGet) checks requests from the node's kubelet, which doesn't guarantee cross-node network reliability.

8. **How can an application scale to handle traffic fluctuations?**

Kubernetes supports Horizontal Pod Autoscaling (HPA) and Vertical Pod Autoscaling (VPA). VPA involves recreating Pods with adjusted resources, limiting its scenarios. HPA is more commonly used, dynamically adjusting Pod counts based on metrics like CPU usage, request rate, or custom metrics. External systems can also trigger scaling by sending requests to the kube-apiserver.

9. **When you execute kubectl exec -it <pod> -- bash, are you logging into the pod?**

No, kubectl exec requires specifying a container (defaulting to the only container in a single-container Pod). Pods are collections of isolated Linux namespaces. Containers share Network, IPC, and UTS namespaces, while PID and Mount namespaces remain separate. kubectl exec -it <pod> -- bash starts a new bash process in the target container's isolated environment but doesn't "log in" to the Pod.

10. **How would you troubleshoot if a container in a Pod repeatedly exits and restarts?**

If a container repeatedly crashes, kubectl exec won't work. Instead, examine node and container logs, inspect the Pod's status, and use kubectl debug to start a temporary container for investigating the environment and dependencies.

Source: https://medium.com/@rifewang/kubernetes-10-questions-to-test-your-understanding-of-k8s-c2860c9f3cbf
