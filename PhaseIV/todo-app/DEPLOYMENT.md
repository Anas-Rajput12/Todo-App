# Todo-App Local Deployment Guide for Minikube

This guide walks you through deploying the Todo-App to Minikube using Helm charts.

## Prerequisites

- Minikube installed and running
- Helm 3.x installed
- Docker images built for backend and frontend

## Quick Start

### 1. Ensure Minikube is Running

```bash
minikube status
```

If not running:
```bash
minikube start
```

### 2. Load Docker Images into Minikube

Since you've already built the images, load them into Minikube:

```bash
# Option A: Load existing images
minikube image load todo-app-backend:latest
minikube image load todo-app-frontend:latest

# Option B: Build directly in Minikube's Docker environment
# Windows PowerShell:
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
docker build -t todo-app-backend:latest ./backend
docker build -t todo-app-frontend:latest ./frontend

# Or use eval on Git Bash:
eval $(minikube -p minikube docker-env)
docker build -t todo-app-backend:latest ./backend
docker build -t todo-app-frontend:latest ./frontend
```

### 3. Enable Ingress Addon (Optional but Recommended)

```bash
minikube addons enable ingress
minikube addons enable metrics-server
```

### 4. Deploy with Helm

```bash
# Navigate to the chart directory
cd todo-app

# Install the chart
helm install todo-app . --namespace todo-app --create-namespace

# Or upgrade if already installed
helm upgrade todo-app . --namespace todo-app
```

### 5. Access the Application

#### Option A: Via Ingress (Recommended)

1. Get Minikube IP:
   ```bash
   minikube ip
   ```

2. Add to hosts file (`C:\Windows\System32\drivers\etc\hosts`):
   ```
   <minikube-ip> todo-app.local
   ```

3. Access:
   - Frontend: http://todo-app.local/
   - Backend API: http://todo-app.local/api

#### Option B: Via NodePort

- Frontend: http://\<minikube-ip\>:30002
- Backend API: http://\<minikube-ip\>:30001

Get the IP:
```bash
minikube ip
```

#### Option C: Via Port Forwarding

```bash
# Frontend
kubectl port-forward -n todo-app svc/todo-app-frontend 3000:3000

# Backend (in another terminal)
kubectl port-forward -n todo-app svc/todo-app-backend 8000:8000
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### 6. Verify Deployment

```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check ingress
kubectl get ingress -n todo-app

# View logs
kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f

# Run connection tests
helm test todo-app -n todo-app
```

## Configuration

### Update Image Names

Edit `values.yaml` to match your actual image names:

```yaml
backend:
  image:
    repository: your-registry/todo-app-backend
    tag: latest

frontend:
  image:
    repository: your-registry/todo-app-frontend
    tag: latest
```

### Environment Variables

Add environment variables in `values.yaml`:

```yaml
backend:
  env:
    - name: DATABASE_URL
      value: "postgresql://user:pass@db:5432/todos"
    - name: SECRET_KEY
      value: "your-secret-key"

frontend:
  env:
    - name: NEXT_PUBLIC_API_BASE_URL
      value: "http://todo-app-backend:8000"
```

## Uninstall

```bash
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
```

## Troubleshooting

### ImagePullBackOff Error

Ensure images are loaded in Minikube:
```bash
minikube image list | grep todo-app
```

### Ingress Not Working

1. Verify ingress addon is enabled:
   ```bash
   minikube addons list | grep ingress
   ```

2. Check ingress controller:
   ```bash
   kubectl get pods -n ingress-nginx
   ```

### Services Not Accessible

Check service configuration:
```bash
kubectl describe svc -n todo-app
```

### View All Resources

```bash
kubectl get all -n todo-app
```

## Deployment Commands Summary

```bash
# Start Minikube
minikube start

# Load images
minikube image load todo-app-backend:latest
minikube image load todo-app-frontend:latest

# Enable addons
minikube addons enable ingress

# Deploy
helm install todo-app ./todo-app -n todo-app --create-namespace

# Check status
kubectl get all -n todo-app

# Access via browser
minikube service todo-app-frontend -n todo-app --url

# Cleanup
helm uninstall todo-app -n todo-app
minikube stop
```

## Next Steps

1. Configure persistent storage for database
2. Set up ConfigMaps for environment-specific settings
3. Add secrets management for sensitive data
4. Configure horizontal pod autoscaling for production
