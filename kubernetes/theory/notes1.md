what is the difference between k8s kubernetes requets and limits

**Requests**:
- Define the minimum guaranteed resources that a container needs to run
- Kubernetes uses these values for scheduling decisions
- The node must have at least this much resource available to schedule the pod
- Example: If you set CPU request to 0.5, K8s guarantees half a CPU core

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "0.5"
```

**Limits**:
- Define the maximum amount of resources a container can use
- Container cannot exceed these boundaries
- If a container tries to use more CPU than its limit, it gets throttled
- If it exceeds memory limit, it might be terminated (OOMKilled)

```yaml
resources:
  limits:
    memory: "512Mi"
    cpu: "1"
```

Key differences:
1. **Purpose**:
   - Requests: Resource planning and scheduling
   - Limits: Resource constraints and protection

2. **Guarantee**:
   - Requests: Guaranteed minimum
   - Limits: Hard ceiling

3. **Behavior**:
   - Requests: Used for pod scheduling
   - Limits: Used for runtime enforcement

IMP: The resources key is added to specify the limits and requests. The Pod will only be scheduled on a Node with 0.35 CPU cores and 10MiB of memory available. It's important to note that the scheduler doesn't consider the actual resource utilization of the node. Rather, it bases its decision upon the sum of container resource requests on the node. For example, if a container requests all the CPU of a node but is actually 0% CPU, the scheduler would treat the node as not having any CPU available. In the context of this lab, the load Pod is consuming 2 CPUs on a Node but because it didn't make any request for the CPU, its usage doesn't impact following scheduling requests.
