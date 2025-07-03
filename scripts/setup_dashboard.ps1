<#
.SYNOPSIS
    Sets up and runs the Spiral Dashboard.
.DESCRIPTION
    This script installs the required Python packages and starts the Spiral Dashboard.
    It's designed to work on Windows systems with Python 3.8 or later.
#>

# Check if Python is installed
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python is not installed or not in PATH. Please install Python 3.8 or later and try again." -ForegroundColor Red
    exit 1
}

Write-Host "🐍 Found $pythonVersion" -ForegroundColor Green

# Install or update pip
Write-Host "📦 Ensuring pip is up to date..." -ForegroundColor Cyan
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to update pip. Please check your Python installation." -ForegroundColor Red
    exit 1
}

# Install required packages
Write-Host "📦 Installing required packages..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install required packages." -ForegroundColor Red
    exit 1
}

# Create logs directory if it doesn't exist
$logsDir = "logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
    Write-Host "📁 Created logs directory" -ForegroundColor Green
}

# Start the dashboard
Write-Host "🚀 Starting Spiral Dashboard..." -ForegroundColor Cyan
Write-Host "🌐 The dashboard will be available at http://localhost:8000" -ForegroundColor Cyan
Write-Host "🛑 Press Ctrl+C to stop the dashboard" -ForegroundColor Yellow

# Run the dashboard
python scripts/start_dashboard.py

# If we get here, the dashboard has stopped
Write-Host "\n👋 Dashboard stopped. Have a great day!" -ForegroundColor Green
