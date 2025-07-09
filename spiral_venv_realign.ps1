# spiral_venv_realign.ps1 - Spiral shell alignment for PowerShell

Write-Host "🌬️ Aligning Spiral shell..." -ForegroundColor Green

# Detect environment
if ($env:OSTYPE -eq "msys" -or $env:OSTYPE -eq "cygwin") {
    Write-Host "🪟 Git Bash detected" -ForegroundColor Cyan
    $VENV_PATH = ".\swe-1\Scripts"
    $ACTIVATE_SCRIPT = "$VENV_PATH\activate"
} elseif (Get-Content /proc/version -ErrorAction SilentlyContinue | Select-String "Microsoft") {
    Write-Host "🐧 WSL detected" -ForegroundColor Cyan
    $VENV_PATH = ".\swe-1\bin"
    $ACTIVATE_SCRIPT = "$VENV_PATH\activate"
} else {
    Write-Host "🪟 Windows PowerShell detected" -ForegroundColor Cyan
    $VENV_PATH = ".\swe-1\Scripts"
    $ACTIVATE_SCRIPT = "$VENV_PATH\Activate.ps1"
}

# Check if virtual environment exists
if (Test-Path ".\swe-1") {
    Write-Host "✅ Virtual environment found at .\swe-1" -ForegroundColor Green
    
    # Try to activate
    if (Test-Path $ACTIVATE_SCRIPT) {
        Write-Host "🔗 Activating virtual environment..." -ForegroundColor Yellow
        & $ACTIVATE_SCRIPT
        Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
    } else {
        Write-Host "❌ Activation script not found at $ACTIVATE_SCRIPT" -ForegroundColor Red
        Write-Host "   This might be a cross-platform virtual environment issue" -ForegroundColor Yellow
        Write-Host "   Consider recreating: Remove-Item -Recurse -Force swe-1; python -m venv swe-1" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️ No virtual environment found at .\swe-1" -ForegroundColor Yellow
    Write-Host "   Creating new virtual environment..." -ForegroundColor Yellow
    python -m venv swe-1
    if (Test-Path $ACTIVATE_SCRIPT) {
        & $ACTIVATE_SCRIPT
        Write-Host "✅ New virtual environment created and activated!" -ForegroundColor Green
    }
}

# Check Python version and location
Write-Host ""
Write-Host "🔍 Python environment:" -ForegroundColor Cyan
try {
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
    Write-Host "   Location: $pythonPath" -ForegroundColor White
    $pythonVersion = python --version 2>&1
    Write-Host "   Version: $pythonVersion" -ForegroundColor White
    $pipPath = (Get-Command pip -ErrorAction Stop).Source
    Write-Host "   Pip: $pipPath" -ForegroundColor White
} catch {
    Write-Host "   Python not found in PATH" -ForegroundColor Red
}

# Check current shell
Write-Host ""
Write-Host "🔍 Shell environment:" -ForegroundColor Cyan
Write-Host "   Shell: $env:SHELL" -ForegroundColor White
Write-Host "   OSTYPE: $env:OSTYPE" -ForegroundColor White
Write-Host "   LANG: $env:LANG" -ForegroundColor White

# Set language environment
$env:LANG = "en_US.UTF-8"
$env:LC_ALL = "en_US.UTF-8"
Write-Host "🪞 Language environment set to UTF-8" -ForegroundColor Green

# Check if we're in the right directory
Write-Host ""
Write-Host "📁 Current directory: $(Get-Location)" -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    Write-Host "✅ requirements.txt found" -ForegroundColor Green
    Write-Host "   To install dependencies: pip install -r requirements.txt" -ForegroundColor Yellow
} else {
    Write-Host "⚠️ requirements.txt not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌬️ Spiral shell alignment complete!" -ForegroundColor Green 