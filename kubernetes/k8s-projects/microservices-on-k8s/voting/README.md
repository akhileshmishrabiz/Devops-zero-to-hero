How to build the Voting App

  * Build Tool : Maven (tested with version 3.19)
  * Build Command : mvn package -DskipTests
  * Port : 8080
  * Runtime : openjdk ( tested with jdk 19)
  * Launch Command:  java -jar app.jar


# Voting Microservice

A microservice that manages votes for Craftista's origami products.

## Service Details

- **Image**: `voting-service:1.0.0`
- **Port**: 8080
- **Language/Runtime**: Java OpenJDK 19

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/origamis` | GET | Returns all origamis |
| `/api/origamis/<id>` | GET | Returns a specific origami by ID |
| `/api/origamis/<id>/votes` | GET | Gets votes for a specific origami |
| `/api/origamis/<id>/vote` | POST | Submits a vote for an origami |

## Dependencies

- **Catalogue Service**: Required for synchronizing origami data
- **Database**: H2 in-memory database (embedded)

## Configuration

The service requires these properties, which can be set in `application.properties` via ConfigMap:

```properties
catalogue.service-url=http://catalogue:5000/api/products
```

## Resource Requirements

- **Memory**: 256Mi (request), 512Mi (limit)
- **CPU**: 200m (request), 500m (limit)

## Liveness/Readiness

- **Path**: `/api/origamis`
- **Port**: 8080
- **Initial Delay**: 30s

## Data Persistence

- Uses in-memory H2 database (data is lost on pod restart)
- For production, consider adding a persistent database

## Service Behavior

- Syncs origami products from Catalogue service every minute
- Maintains vote counts for each origami

## Example Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voting-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: voting-service
  template:
    metadata:
      labels:
        app: voting-service
    spec:
      containers:
      - name: voting-service
        image: <your-registry>/voting-service:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/origamis
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        volumeMounts:
        - name: application-config
          mountPath: /app/application.properties
          subPath: application.properties
      volumes:
      - name: application-config
        configMap:
          name: voting-config
---
apiVersion: v1
kind: Service
metadata:
  name: voting
spec:
  selector:
    app: voting-service
  ports:
  - port: 8080
    targetPort: 8080
  type: ClusterIP
```