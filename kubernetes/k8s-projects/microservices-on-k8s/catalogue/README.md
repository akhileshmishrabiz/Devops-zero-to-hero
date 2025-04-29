How to build Python Flask based Catalogue App

  * Python version: latest
  * Build Tool : pip
  * Build Command : pip install -r requirements.txt
  * Port : 5000
  * Launch Command : gunicorn app:app --bind 0.0.0.0:5000  


# Catalogue Microservice

A microservice that provides product catalogue information for Craftista.

## Service Details

- **Image**: `catalogue-service:1.0.0`
- **Port**: 5000
- **Language/Runtime**: Python 3.11

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products` | GET | Returns all products |
| `/api/products/<id>` | GET | Returns a specific product by ID |

## Dependencies

- **Database**: PostgreSQL (optional, configurable via `data_source` setting)

## Configuration

Mount this as a ConfigMap at `/app/config.json`:

```json
{
    "app_version": "1.0.0",
    "data_source": "json",
    "db_host": "catalogue-db", 
    "db_name": "catalogue",
    "db_user": "devops",
    "db_password": "devops"
}
```

### Configuration Options:
- `data_source`: Set to `"json"` to use the embedded JSON file or `"db"` to use PostgreSQL
- Database credentials only required if `data_source` is set to `"db"`

## Resource Requirements

- **Memory**: 128Mi (request), 256Mi (limit)
- **CPU**: 100m (request), 200m (limit)

## Liveness/Readiness

- **Path**: `/`
- **Port**: 5000
- **Initial Delay**: 10s

## Storage

- Static files should be mounted at `/app/static`
- Templates should be mounted at `/app/templates`
- Product data is in `/app/products.json`

## Example Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: catalogue-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: catalogue-service
  template:
    metadata:
      labels:
        app: catalogue-service
    spec:
      containers:
      - name: catalogue-service
        image: <your-registry>/catalogue-service:1.0.0
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 5000
          initialDelaySeconds: 10
        volumeMounts:
        - name: config
          mountPath: /app/config.json
          subPath: config.json
      volumes:
      - name: config
        configMap:
          name: catalogue-config
---
apiVersion: v1
kind: Service
metadata:
  name: catalogue
spec:
  selector:
    app: catalogue-service
  ports:
  - port: 5000
    targetPort: 5000
  type: ClusterIP
```