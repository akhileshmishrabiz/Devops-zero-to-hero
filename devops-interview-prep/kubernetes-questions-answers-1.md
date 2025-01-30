# Kubernetes Interview Questions & Answers

### Q1: How do you handle Kubernetes upgrades without causing downtime in production?
**Answer:** To handle Kubernetes upgrades without downtime:
1. Back up etcd data and cluster state
2. Use rolling updates for upgrading nodes and control plane components
3. Implement proper pod disruption budgets (PDB)
4. Test upgrades in staging first
5. Monitor metrics during upgrade
6. Have rollback plans ready
7. Use node pools for better isolation

### Q2: Explain the Kubernetes architecture and its components.
**Answer:** Kubernetes architecture has two main parts:

Control Plane Components:
- API Server: Central management point
- etcd: Distributed data store
- Scheduler: Assigns pods to nodes
- Controller Manager: Maintains desired state

Worker Node Components:
- Kubelet: Node agent
- Container Runtime: Runs containers
- Kube-proxy: Handles networking

### Q3: How to set up a Kubernetes pod with multiple containers, giving one container full S3 access and another container IAM access?
**Answer:** You can achieve this by:
1. Creating IAM roles with appropriate permissions
2. Using IAM roles for service accounts (IRSA)
3. Configuring the pod with multiple containers
4. Setting up environment variables and AWS credentials as secrets
5. Mounting AWS credentials to specific containers
6. Implementing least privilege principle for security

### Q4: What is the difference between Docker Swarm and Kubernetes?
**Answer:** Key differences include:
1. Complexity: Swarm is simpler, Kubernetes is more complex but powerful
2. Features: Kubernetes has more features and extensive ecosystem
3. Scaling: Kubernetes offers more advanced scaling options
4. Load Balancing: Kubernetes has more sophisticated options
5. Learning Curve: Swarm is easier to learn, Kubernetes takes more time

### Q5: How will you reduce the Docker image size?
**Answer:** To reduce Docker image size:
1. Use multi-stage builds
2. Choose smaller base images (alpine/slim variants)
3. Combine RUN commands to reduce layers
4. Remove unnecessary files and packages
5. Use .dockerignore file
6. Clean up package manager cache

### Q6: Will data on the container be lost when the Docker container exits?
**Answer:** Yes, by default, data in containers is ephemeral and will be lost when the container exits. To persist data, you can use:
1. Volumes
2. Bind mounts
3. Persistent Volume Claims (PVC)
4. tmpfs mounts (temporary, memory-based storage)

### Q7: What is a Kubernetes Deployment, and how does it differ from a ReplicaSet?
**Answer:** A Deployment manages ReplicaSets and provides declarative updates for Pods.
- Deployment provides rolling updates and rollbacks
- ReplicaSet ensures a specified number of pod replicas are running
- Deployment tracks version history
- Deployment can pause/resume updates
- ReplicaSet doesn't support rolling updates on its own

### Q8: Can you explain the concept of self-healing in Kubernetes?
**Answer:** Self-healing in Kubernetes means:
1. Automatically restarts failed containers
2. Replaces and reschedules pods when nodes die
3. Kills and restarts pods that don't respond to health checks
4. Prevents traffic to pods until they're ready to serve

### Q9: How does Kubernetes handle network communication between containers?
**Answer:** Kubernetes handles network communication through:
1. Pod networking (containers within pod share network namespace)
2. Service discovery (DNS-based)
3. Network policies for traffic control
4. CNI plugins for implementation
5. Load balancing through Services

### Q10: What is the difference between DaemonSet and StatefulSet?
**Answer:**
DaemonSet:
- Runs one pod per node
- Used for node-level operations
- Typically for monitoring, logging

StatefulSet:
- Maintains unique identity for each pod
- Provides ordered deployment and scaling
- Used for stateful applications
- Provides stable network identifiers

### Q11: How does a NodePort service work?
**Answer:** NodePort service:
1. Exposes the service on a static port (30000-32767)
2. Makes service accessible on every node's IP
3. Forwards traffic to appropriate pods
4. Provides load balancing automatically
5. Can be accessed from outside the cluster

### Q12: What strategies would you use to manage secrets in Kubernetes?
**Answer:** Strategies for secret management:
1. Use Kubernetes native secrets
2. Implement external secret managers (HashiCorp Vault, AWS Secrets Manager)
3. Encrypt secrets at rest
4. Use RBAC for access control
5. Implement secret rotation
6. Monitor secret usage

### Q13: Can you discuss the implications of running privileged containers and how to mitigate the risks?
**Answer:** Privileged containers risks and mitigation:

Risks:
- Full host access
- Security bypass potential
- System compromise risk

Mitigation:
1. Use security contexts
2. Implement pod security policies
3. Apply least privilege principle
4. Regular security audits

### Q14: How would you approach monitoring and logging in a Kubernetes environment?
**Answer:** For monitoring and logging:

Monitoring:
1. Use Prometheus for metrics collection
2. Grafana for visualization
3. AlertManager for alerts

Logging:
1. Use EFK/ELK Stack or Loki
2. Implement log aggregation
3. Set up log retention policies
4. Configure monitoring dashboards

### Q15: How can horizontal pod autoscaling be implemented in Kubernetes?
**Answer:** To implement HPA:
1. Deploy metrics server
2. Configure resource requests/limits
3. Set up HPA configuration with metrics
4. Define min/max replicas
5. Choose scaling metrics (CPU, memory, custom)
6. Set target utilization thresholds

### Q16: What are service meshes, and how do they enhance microservices architecture?
**Answer:** Service meshes provide:
1. Traffic management
2. Security (mTLS)
3. Observability
4. Policy enforcement
5. Load balancing
6. Circuit breaking
7. Request tracing

Popular options include Istio, Linkerd, and Consul Connect.

### Q17: Describe a scenario where you would use admission controllers in Kubernetes.
**Answer:** Common admission controller scenarios:
1. Enforcing resource limits
2. Validating security contexts
3. Injecting sidecar containers
4. Policy enforcement
5. Custom validations
6. Security compliance checks
7. Resource quota management
