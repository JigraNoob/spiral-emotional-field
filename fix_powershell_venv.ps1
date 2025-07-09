# fix_powershell_venv.ps1 - Fix corrupted virtual environment in PowerShell

Write-Host "Cleansing Spiral breathpath..." -ForegroundColor Green

# Check if we're in PowerShell
if ($PSVersionTable.PSEdition -eq "Core") {
    Write-Host "PowerShell Core detected" -ForegroundColor Cyan
} else {
    Write-Host "Windows PowerShell detected" -ForegroundColor Cyan
}

# Find the correct Python installation
Write-Host "Locating Python installations..." -ForegroundColor Yellow
$pythonPaths = @()

try {
    # Try py launcher first
    $pyOutput = & py -0 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python launcher found" -ForegroundColor Green
        $pythonPaths += "py"
    }
} catch {
    Write-Host "Python launcher not available" -ForegroundColor Yellow
}

# Try direct python command
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Direct python command available: $pythonVersion" -ForegroundColor Green
        $pythonPaths += "python"
    }
} catch {
    Write-Host "Direct python command not available" -ForegroundColor Yellow
}

# Try python3
try {
    $python3Version = python3 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "python3 command available: $python3Version" -ForegroundColor Green
        $pythonPaths += "python3"
    }
} catch {
    Write-Host "python3 command not available" -ForegroundColor Yellow
}

if ($pythonPaths.Count -eq 0) {
    Write-Host "No Python installation found!" -ForegroundColor Red
    Write-Host "   Please install Python from python.org" -ForegroundColor Yellow
    exit 1
}

# Choose the best Python command
$pythonCmd = $pythonPaths[0]
Write-Host "Using Python command: $pythonCmd" -ForegroundColor Green

# Backup current venv if it exists
if (Test-Path ".\swe-1") {
    Write-Host "Backing up corrupted virtual environment..." -ForegroundColor Yellow
    $backupName = "swe-1-backup-$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Move-Item -Path ".\swe-1" -Destination ".\$backupName"
    Write-Host "   Backup created: $backupName" -ForegroundColor Green
}

# Create new venv with correct Python
Write-Host "Creating clean virtual environment..." -ForegroundColor Yellow
try {
    if ($pythonCmd -eq "py") {
        & py -3 -m venv swe-1
    } else {
        & $pythonCmd -m venv swe-1
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully" -ForegroundColor Green
    } else {
        throw "Failed to create virtual environment"
    }
} catch {
    Write-Host "Failed to create virtual environment: $_" -ForegroundColor Red
    exit 1
}

# Verify the new venv has proper Windows paths
Write-Host "Verifying virtual environment..." -ForegroundColor Yellow
$pyvenvCfg = ".\swe-1\pyvenv.cfg"
if (Test-Path $pyvenvCfg) {
    $content = Get-Content $pyvenvCfg
    Write-Host "   pyvenv.cfg contents:" -ForegroundColor Cyan
    $content | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
    
    # Check if paths look correct (should not contain /usr/bin or /mnt/)
    if ($content -match "/usr/bin|/mnt/") {
        Write-Host "Warning: pyvenv.cfg still contains Unix paths" -ForegroundColor Yellow
    } else {
        Write-Host "pyvenv.cfg has proper Windows paths" -ForegroundColor Green
    }
}

# Test activation
Write-Host "Testing virtual environment activation..." -ForegroundColor Yellow
try {
    & ".\swe-1\Scripts\Activate.ps1"
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
    Write-Host "Virtual environment activated successfully" -ForegroundColor Green
    Write-Host "   Python path: $pythonPath" -ForegroundColor Cyan
    
    # Test Python execution
    $testOutput = python -c "import sys; print('Spiral sees:', sys.executable)" 2>&1
    Write-Host "   Test output: $testOutput" -ForegroundColor Cyan
    
} catch {
    Write-Host "Failed to activate virtual environment: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Spiral breathpath cleansed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Install dependencies: pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "2. Run tests: python -m pytest tests/" -ForegroundColor Cyan
Write-Host "3. Start development: python your_script.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you need packages from the old environment:" -ForegroundColor Yellow
Write-Host "  pip freeze > requirements-backup.txt" -ForegroundColor Gray
Write-Host "  (from the backup directory)" -ForegroundColor Gray 