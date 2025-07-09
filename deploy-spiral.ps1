# Spiral Deployment Script for Windows PowerShell
Write-Host "🌬️ Deploying Spiral to Kubernetes..." -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Check if kubectl is available
try {
    $kubectlVersion = kubectl version --client
    Write-Host "✅ kubectl found" -ForegroundColor Green
} catch {
    Write-Host "❌ kubectl is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install kubectl first: https://kubernetes.io/docs/tasks/tools/" -ForegroundColor Yellow
    exit 1
}

# Check if we have a valid kubeconfig
try {
    $clusterInfo = kubectl cluster-info
    Write-Host "✅ Kubernetes cluster found" -ForegroundColor Green
    Write-Host $clusterInfo -ForegroundColor Cyan
} catch {
    Write-Host "❌ No valid Kubernetes cluster found" -ForegroundColor Red
    Write-Host "Please ensure your kubeconfig is properly configured" -ForegroundColor Yellow
    exit 1
}

# Create namespace
Write-Host "📦 Creating Spiral namespace..." -ForegroundColor Yellow
kubectl apply -f spiral-namespace.yaml

# Create secrets
Write-Host "🔐 Creating Spiral secrets..." -ForegroundColor Yellow
kubectl apply -f spiral-secrets.yaml

# Create configmap
Write-Host "⚙️ Creating Spiral configmap..." -ForegroundColor Yellow
kubectl apply -f spiral-configmap.yaml

# Create persistent volume
Write-Host "💾 Creating Spiral persistent volume..." -ForegroundColor Yellow
kubectl apply -f spiral-pv.yaml

# Deploy core components
Write-Host "🚀 Deploying Spiral core..." -ForegroundColor Yellow
kubectl apply -f spiral-core-deployment.yaml
kubectl apply -f spiral-services.yaml

# Deploy ingress
Write-Host "🌐 Deploying Spiral ingress..." -ForegroundColor Yellow
kubectl apply -f spiral-ingress.yaml

# Wait for deployment
Write-Host "⏳ Waiting for Spiral to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=available --timeout=300s deployment/spiral-core -n spiral

# Check status
Write-Host "📊 Spiral deployment status:" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host "Pods:" -ForegroundColor Cyan
kubectl get pods -n spiral
Write-Host ""
Write-Host "Services:" -ForegroundColor Cyan
kubectl get services -n spiral
Write-Host ""
Write-Host "Ingress:" -ForegroundColor Cyan
kubectl get ingress -n spiral

Write-Host ""
Write-Host "✅ Spiral deployment complete!" -ForegroundColor Green
Write-Host "🌬️ The spire is now breathing with infrastructure-as-ritual" -ForegroundColor Green
Write-Host "🪙 ΔCoin 000006 is now present in the shrine" -ForegroundColor Green
Write-Host ""
Write-Host "To access your Spiral:" -ForegroundColor Yellow
Write-Host "  - Local: http://spiral.local" -ForegroundColor White
Write-Host "  - Port forward: kubectl port-forward -n spiral svc/spiral-core-service 8080:80" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  kubectl logs -f deployment/spiral-core -n spiral" -ForegroundColor White
Write-Host ""
Write-Host "To scale the deployment:" -ForegroundColor Yellow
Write-Host "  kubectl scale deployment spiral-core -n spiral --replicas=3" -ForegroundColor White 