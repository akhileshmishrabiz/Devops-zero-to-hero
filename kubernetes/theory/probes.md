If a Pod is in a Running state it does not necessarily mean the Pod is ready to use or that the Pod is operating as you would expect. For example, a running Pod may not be ready to accept requests or may have entered into an internal failed state, such as a deadlock, preventing it to make progress on new requests. Kubernetes introduces probes for containers to detect when Pods are in such states. More specifically:

Readiness probes are used to detect when a Pod is unable to serve traffic, such as during startup when large amounts of data are being loaded or caches are being warmed. When a readiness probe fails, it means that the Pod needs more time to become ready to serve traffic. When the Pod is accessed through a Kubernetes Service, the Service will not serve traffic to any Pods that have a failing readiness probe. 

Liveness probes are used to detect when a Pod fails to make progress after entering a broken state, such as deadlock. The issues causing the Pod to enter such a broken state are bugs, but by detecting a Pod is in a broken state allows Kubernetes to restart the Pod and allow progress to be made, perhaps only temporarily until arriving at the broken state again. The application availability is improved compared to leaving the Pod in the broken state.

Startup probes are used when an application starts slowly and may otherwise be killed due to failed liveness probes. The startup probe runs before both readiness and liveness probes. The startup probe can be configured with a startup time that is longer than the time needed to detect a broken state for a container after it has started.

Readiness and Liveness probes run for the entire lifetime of the container they are declared in. Startup probes only run until they first succeed. A container can define up to one of each type of probe. All probes are also configured the same way. The only difference is how a probe failure is interpreted

** There are three types of actions a probe can take to assess the readiness of a Pod's container: **

exec: Issue a command in the container. If the exit code is zero the container is a success, otherwise it is a failed probe.

httpGet: Send a HTTP GET request to the container at a specified path and port. If the HTTP response status code is a 2xx or 3xx then the container is a success, otherwise, it is a failure.

tcpSocket: Attempt to open a socket to the container on a specified port. If the connection cannot be established, the probe fails.

The number of consecutive successes is configured via the successThreshold field and the number of consecutive failures required to transition from success to failure is failureThreshold. The probe runs every periodSeconds and each probe will wait up to timeoutSeconds to complete.


## In Kubernetes, "Probes" are a way for the kubelet to check the health of a container running inside a pod. There are three main types of probes:

1. **Liveness Probes**:
   - Checks if the container is running and healthy
   - If the liveness probe fails, Kubernetes will restart the container
   - Useful for detecting and recovering from application deadlocks or other runtime issues

2. **Readiness Probes**:
   - Checks if the container is ready to accept traffic
   - If the readiness probe fails, Kubernetes will not send traffic to the pod
   - Useful for ensuring the application is fully initialized and ready to handle requests before going live

3. **Startup Probes**:
   - Checks if the application in the container has started up successfully
   - Gives the application time to start up without being killed by the liveness probe
   - Useful for slow starting applications that need more time to initialize

Probe Types:

- **HTTP GET**: Makes an HTTP GET request to a specified path on the container
- **TCP Socket**: Attempts to open a TCP connection to a specified port on the container
- **Exec**: Executes a command inside the container and checks the exit code

Example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 3600']
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 3
      periodSeconds: 5
    readinessProbe:
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 5
      periodSeconds: 10
```

Key points:
- Liveness probe checks `/healthz` endpoint every 5 seconds
- Readiness probe executes `cat /tmp/healthy` every 10 seconds
- `initialDelaySeconds` gives time for the app to start up

Probes help ensure your application is healthy and can handle traffic reliably in a Kubernetes environment.
