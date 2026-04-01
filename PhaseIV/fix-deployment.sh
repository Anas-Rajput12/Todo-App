#!/bin/bash
# Fix Frontend and Backend Connection - Run this in WSL

set -e

echo "=== Fixing Frontend-Backend Connection ==="

# Navigate to project directory
cd /mnt/c/users/megabyte/desktop/todo-app/phaseii

echo "Step 1: Setting up Minikube Docker environment..."
eval $(minikube -p minikube docker-env)

echo "Step 2: Building frontend image with relative API paths..."
docker build -t todo-app-frontend:latest ./frontend

echo "Step 3: Loading image into Minikube (if needed)..."
minikube image load todo-app-frontend:latest || true

echo "Step 4: Applying updated ingress configuration..."
kubectl apply -f todo-app/ingress.yaml

echo "Step 5: Restarting frontend deployment..."
kubectl rollout restart deployment todo-apps-frontend

echo "Step 6: Waiting for deployment to complete..."
kubectl rollout status deployment todo-apps-frontend

echo "Step 7: Verifying pods..."
kubectl get pods

echo "Step 8: Getting Minikube IP..."
minikube ip

echo ""
echo "=== Deployment Complete! ==="
echo ""
echo "Access your application at:"
echo "  http://todo-app.local/"
echo ""
echo "Or directly via IP (replace with your Minikube IP):"
echo "  http://$(minikube ip)/"
echo ""
echo "API endpoints will be available at:"
echo "  http://$(minikube ip)/api/v1/auth/signup"
echo "  http://$(minikube ip)/api/v1/auth/login"
echo "  http://$(minikube ip)/api/docs"
echo ""
echo "If you're still seeing errors, add this to your hosts file:"
echo "  $(minikube ip) todo-app.local"
echo ""
