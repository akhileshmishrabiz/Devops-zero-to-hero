How to Build Recommendation App 

  * Build Tool : go (Tested with version 1.20)
  * Build Command : go build -o app
  * Port: 8080
  * Launch Command: ./app
 


 # Recommendation Microservice

A microservice that provides daily origami recommendations.

## Service Details

- **Image**: `recommendation-service:1.0.0`
- **Port**: 8080
- **Language/Runtime**: Go 1.20

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/origami-of-the-day` | GET | Returns a random origami recommendation |
| `/api/recommendation-status` | GET | Health check endpoint |

## Dependencies

- None (self-contained service)

## Configuration

The service uses a `config.json` file for configuration:

```json
{
    "version": "1.0.0"
}
```

Mount this as a ConfigMap at `/app/config.json`.

## Resource Requirements

- **Memory**: 128Mi (request), 256Mi (limit)
- **CPU**: 100m (request), 200m (limit)

## Liveness/Readiness

- **Path**: `/api/recommendation-status`
- **Port**: 8080
- **Initial Delay**: 10s

## Storage

- Static files should be mounted at `/app/static`
- Templates should be mounted at `/app/templates`

## Build Instructions

```bash
# Build Docker image
docker build -t recommendation-service:1.0.0 .

# Push to registry
docker push <your-registry>/recommendation-service:1.0.0
```

## Example Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recommendation-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: recommendation-service
  template:
    metadata:
      labels:
        app: recommendation-service
    spec:
      containers:
      - name: recommendation-service
        image: <your-registry>/recommendation-service:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /api/recommendation-status
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:
        - name: config
          mountPath: /app/config.json
          subPath: config.json
      volumes:
      - name: config
        configMap:
          name: recommendation-config
---
apiVersion: v1
kind: Service
metadata:
  name: recommendation-service
spec:
  selector:
    app: recommendation-service
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```
