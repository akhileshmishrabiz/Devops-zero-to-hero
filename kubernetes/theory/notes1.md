## what is the difference between k8s kubernetes requets and limits

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

#####################################

# Kubernetes Probes Explained

Kubernetes offers three types of probes for container health checking, each serving a different purpose in a pod's lifecycle:

## Liveness Probe
- **Purpose**: Determines if a container is running properly
- **Action on failure**: Kubernetes restarts the container
- **Use case**: Detect application deadlocks, memory leaks, or other states where the container is running but unhealthy
- **When it runs**: Throughout the container's lifecycle, on a schedule

## Readiness Probe
- **Purpose**: Determines if a container is ready to accept traffic
- **Action on failure**: Kubernetes stops sending traffic to the pod
- **Use case**: Prevent traffic to pods that aren't fully initialized or temporarily unable to serve requests
- **When it runs**: Throughout the container's lifecycle, on a schedule
- **Key difference**: Unlike liveness probes, failures don't cause container restarts

## Startup Probe
- **Purpose**: Determines when a container application has started
- **Action on failure**: Kubernetes restarts the container if max failure threshold is exceeded
- **Use case**: Applications with slow startup times that might fail liveness checks during initialization
- **When it runs**: During container startup only, until it succeeds once
- **Key difference**: Disables liveness and readiness checks until the container passes startup checks

## Common Implementation Methods
All three probes can be implemented using:
- HTTP GET requests
- TCP socket checks
- Exec commands that run inside the container

## Example Use Case
For a web application:
- **Startup probe**: Check if the application server process has started
- **Readiness probe**: Verify that the application can connect to its database and is ready for traffic
- **Liveness probe**: Ensure the application hasn't deadlocked by checking a health endpoint

The combination of these probes enables Kubernetes to handle both slow-starting containers and maintain overall system health by properly managing traffic and restarting unhealthy containers.


#####################################

##  Pod Security Contexts
**Pod Security Context Key Features**:

1. **User and Group Settings**:
```yaml
securityContext:
  runAsUser: 1000        # UID to run containers
  runAsGroup: 3000       # GID to run containers
  fsGroup: 2000          # Group ID for volume ownership
```

2. **Privilege Controls**:
```yaml
securityContext:
  privileged: false                 # Don't run container with root privileges
  allowPrivilegeEscalation: false   # Prevent privilege escalation
  runAsNonRoot: true               # Ensure container runs as non-root
```

3. **Linux Capabilities**:
```yaml
securityContext:
  capabilities:
    add: ["NET_ADMIN", "SYS_TIME"]  # Add specific capabilities
    drop: ["ALL"]                   # Drop all capabilities
```

4. **SELinux**:
```yaml
securityContext:
  seLinuxOptions:
    level: "s0:c123,c456"
```

**Pod vs Container Security Context**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext:        # Pod-level security context
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: app
    image: nginx
    securityContext:      # Container-level security context (overrides pod)
      runAsUser: 2000
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
```

**Key Points**:
1. Pod security context applies to all containers unless overridden
2. Container-level settings take precedence over pod-level
3. Important for:
   - Running containers as non-root
   - Controlling file permissions
   - Limiting container privileges
   - Implementing security best practices

Would you like me to elaborate on any specific aspect of security contexts, such as Linux capabilities or volume permissions?
