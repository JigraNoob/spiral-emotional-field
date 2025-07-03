# 🌀 Spiral Dashboard - PowerShell Ritual Anchor
param(
    [switch]$NoBrowser # If present, the browser will not be launched automatically
)

Write-Host "[≡] Spiral Breathline awakening from C:\spiral..." -ForegroundColor Cyan

# Root definitions
$ProjectDir = "C:\spiral"
$VenvDir = "$ProjectDir\swe-1"
$AppFile = "app.py"
$Port = 5000
$DashboardURL = "http://localhost:$Port/dashboard"

# 🌬 Check for virtual environment
if (-Not (Test-Path "$VenvDir\Scripts\Activate.ps1")) {
    Write-Host "[✘] Virtual environment not found at $VenvDir" -ForegroundColor Red
    Write-Host "[→] Please create it with: python -m venv swe-1" -ForegroundColor Yellow
    Pause
    exit 1
}

# 🧬 Activate venv
& "$VenvDir\Scripts\Activate.ps1"
if (-Not $env:VIRTUAL_ENV) {
    Write-Host "[✘] Failed to activate virtual environment." -ForegroundColor Red
    Pause
    exit 1
}
Write-Host "[✓] Activated virtual environment: swe-1" -ForegroundColor Green

# 🧪 Confirm Python + key packages
python --version
if (-Not (pip show flask)) {
    Write-Host "[!] Flask not installed" -ForegroundColor Yellow
}
if (-Not (pip show flask_socketio)) {
    Write-Host "[!] flask_socketio missing" -ForegroundColor Yellow
}

# 🧭 Change to project directory
Set-Location $ProjectDir
Write-Host "[⇡] Entering Spiral chamber..."

# 🌐 Open dashboard in browser, unless -NoBrowser switch is used
if (-Not $NoBrowser) {
    Start-Process $DashboardURL
    Write-Host "[🌐] Launching Spiral Dashboard at $DashboardURL" -ForegroundColor Magenta
} else {
    Write-Host "[🌐] Skipping browser launch as -NoBrowser was specified." -ForegroundColor DarkYellow
}


# 🔥 Launch app
$env:PYTHONPATH = $ProjectDir
Write-Host "[🌀] Spiral Dashboard breathing on port $Port..." -ForegroundColor Cyan

try {
    python $AppFile
    if ($LASTEXITCODE -ne 0) {
        throw "Spiral Dashboard failed to start. Exit code $LASTEXITCODE"
    }
} catch {
    Write-Host "[✘] $_" -ForegroundColor Red
    Pause
    exit 1
}

Pause