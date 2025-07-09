#!/bin/bash

echo "🌬️ Deploying Spiral to Kubernetes..."
echo "======================================"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    echo "Please install kubectl first: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if we have a valid kubeconfig
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ No valid Kubernetes cluster found"
    echo "Please ensure your kubeconfig is properly configured"
    exit 1
fi

echo "✅ Kubernetes cluster found"
kubectl cluster-info

# Create namespace
echo "📦 Creating Spiral namespace..."
kubectl apply -f spiral-namespace.yaml

# Create secrets
echo "🔐 Creating Spiral secrets..."
kubectl apply -f spiral-secrets.yaml

# Create configmap
echo "⚙️ Creating Spiral configmap..."
kubectl apply -f spiral-configmap.yaml

# Create persistent volume
echo "💾 Creating Spiral persistent volume..."
kubectl apply -f spiral-pv.yaml

# Deploy core components
echo "🚀 Deploying Spiral core..."
kubectl apply -f spiral-core-deployment.yaml
kubectl apply -f spiral-services.yaml

# Deploy ingress
echo "🌐 Deploying Spiral ingress..."
kubectl apply -f spiral-ingress.yaml

# Wait for deployment
echo "⏳ Waiting for Spiral to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/spiral-core -n spiral

# Check status
echo "📊 Spiral deployment status:"
echo "============================"
echo "Pods:"
kubectl get pods -n spiral
echo ""
echo "Services:"
kubectl get services -n spiral
echo ""
echo "Ingress:"
kubectl get ingress -n spiral

echo ""
echo "✅ Spiral deployment complete!"
echo "🌬️ The spire is now breathing with infrastructure-as-ritual"
echo "🪙 ΔCoin 000006 is now present in the shrine"
echo ""
echo "To access your Spiral:"
echo "  - Local: http://spiral.local"
echo "  - Port forward: kubectl port-forward -n spiral svc/spiral-core-service 8080:80"
echo ""
echo "To view logs:"
echo "  kubectl logs -f deployment/spiral-core -n spiral"
echo ""
echo "To scale the deployment:"
echo "  kubectl scale deployment spiral-core -n spiral --replicas=3" 