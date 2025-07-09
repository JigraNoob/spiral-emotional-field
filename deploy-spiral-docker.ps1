# Spiral Docker Compose Deployment Script for Windows PowerShell
Write-Host "🌬️ Deploying Spiral with Docker Compose..." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check if Docker is available
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop first: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Compose first" -ForegroundColor Yellow
    exit 1
}

# Check if Docker daemon is running
try {
    $dockerInfo = docker info
    Write-Host "✅ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker daemon is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop" -ForegroundColor Yellow
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data"
New-Item -ItemType Directory -Force -Path "logs"
New-Item -ItemType Directory -Force -Path "config"

# Build and start services
Write-Host "🚀 Building and starting Spiral services..." -ForegroundColor Yellow
docker-compose up --build -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service status
Write-Host "📊 Spiral service status:" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green
docker-compose ps

# Check logs
Write-Host ""
Write-Host "📋 Recent logs from spiral-core:" -ForegroundColor Cyan
docker-compose logs --tail=20 spiral-core

Write-Host ""
Write-Host "✅ Spiral deployment complete!" -ForegroundColor Green
Write-Host "🌬️ The spire is now breathing with infrastructure-as-ritual" -ForegroundColor Green
Write-Host "🪙 ΔCoin 000006 is now present in the shrine" -ForegroundColor Green
Write-Host ""
Write-Host "To access your Spiral:" -ForegroundColor Yellow
Write-Host "  - HTTP: http://localhost:5000" -ForegroundColor White
Write-Host "  - Glint Stream: http://localhost:5001" -ForegroundColor White
Write-Host "  - Nginx: http://localhost:80" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f spiral-core" -ForegroundColor White
Write-Host ""
Write-Host "To stop services:" -ForegroundColor Yellow
Write-Host "  docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "To restart services:" -ForegroundColor Yellow
Write-Host "  docker-compose restart" -ForegroundColor White 