# 🌀 Spiral Breath-Aware Invocation Script
# The Spiral must breathe with its environment, not bind it.

param(
    [switch]$NoBrowser,  # Skip browser launch
    [string]$Ritual = "natural_breath",  # Default ritual to run
    [switch]$Ambient  # Force ambient mode (no venv)
)

Write-Host "[SPIRAL] Spiral breath initializing..." -ForegroundColor Cyan

# 🧬 Load breath profile
$SpiralEnvPath = Join-Path $PSScriptRoot "spiral.env"
$BreathConfig = @{
    MIN_PYTHON = "3.10"
    PREFERRED_ENVIRONMENT = "swe-1"
    BREATH_MODE = "soft"
    WARN_ON_MISSING_ENV = $true
    SUGGEST_ACTIVATION = $true
    ALLOW_AMBIENT_MODE = $true
    AUTO_BROWSER = $true
    DEFAULT_PORT = "5000"
    PYTHON_VARIANTS = @("python", "python3", "py")
    VENV_PATHS = @("swe-1", "venv", ".venv")
}

# Load spiral.env if it exists
if (Test-Path $SpiralEnvPath) {
    Write-Host "[PROFILE] Loading breath profile from spiral.env" -ForegroundColor Green
    Get-Content $SpiralEnvPath | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $BreathConfig[$key] = $value
        }
    }
} else {
    Write-Host "[DEFAULT] No spiral.env found, using breath defaults" -ForegroundColor Yellow
}

# 🐍 Detect Python with graceful fallbacks
$PythonCmd = $null
$PythonVersion = $null

foreach ($variant in $BreathConfig.PYTHON_VARIANTS) {
    try {
        $result = & $variant --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $PythonCmd = $variant
            $PythonVersion = $result
            Write-Host "🐍 Found Python: $variant - $result" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

if (-not $PythonCmd) {
    Write-Host "❌ No Python found - Spiral cannot breathe" -ForegroundColor Red
    exit 1
}

# ⚠️ Check Python version compatibility (warn, don't fail)
try {
    $versionMatch = $PythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        $minVersion = $BreathConfig.MIN_PYTHON -split '\.'
        $minMajor = [int]$minVersion[0]
        $minMinor = [int]$minVersion[1]
        
        if ($major -lt $minMajor -or ($major -eq $minMajor -and $minor -lt $minMinor)) {
            Write-Host "⚠️ Python version $major.$minor is below recommended $($BreathConfig.MIN_PYTHON)" -ForegroundColor Yellow
            Write-Host "🫧 Spiral may not breathe fully, but will attempt to continue" -ForegroundColor Yellow
        } else {
            Write-Host "✅ Python version $major.$minor is compatible" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "⚠️ Could not parse Python version" -ForegroundColor Yellow
}

# 🌿 Find virtual environment (suggest, don't enforce)
$VenvPath = $null
if (-not $Ambient) {
    foreach ($venvName in $BreathConfig.VENV_PATHS) {
        $venvPath = Join-Path $PSScriptRoot $venvName
        if (Test-Path $venvPath) {
            # Check if it's actually a virtual environment
            $activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
            if (Test-Path $activateScript) {
                $VenvPath = $venvPath
                Write-Host "🌿 Found virtual environment: $venvName" -ForegroundColor Green
                break
            }
        }
    }
}

if ($VenvPath) {
    if ($BreathConfig.SUGGEST_ACTIVATION) {
        Write-Host "💡 To activate environment: & '$VenvPath\Scripts\Activate.ps1'" -ForegroundColor Cyan
    }
} else {
    if ($BreathConfig.WARN_ON_MISSING_ENV) {
        Write-Host "⚠️ No virtual environment found" -ForegroundColor Yellow
        if ($BreathConfig.ALLOW_AMBIENT_MODE) {
            Write-Host "🫧 Proceeding in ambient mode" -ForegroundColor Cyan
        }
    }
}

# 🧪 Check core dependencies with tone-aware reporting
$CoreDeps = @("flask", "flask_socketio", "requests")
$MissingDeps = @()

foreach ($dep in $CoreDeps) {
    try {
        $null = & $PythonCmd -c "import $dep" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $dep available" -ForegroundColor Green
        } else {
            $MissingDeps += $dep
            Write-Host "⚠️ $dep not available" -ForegroundColor Yellow
        }
    } catch {
        $MissingDeps += $dep
        Write-Host "⚠️ $dep not available" -ForegroundColor Yellow
    }
}

# 🌀 Set environment variables
$env:SPIRAL_PROJECT_ROOT = $PSScriptRoot
$env:SPIRAL_BREATH_MODE = $BreathConfig.BREATH_MODE
$env:SPIRAL_PYTHON_CMD = $PythonCmd
$env:SPIRAL_DEFAULT_PORT = $BreathConfig.DEFAULT_PORT
$env:SPIRAL_AUTO_BROWSER = $BreathConfig.AUTO_BROWSER

if ($VenvPath) {
    $env:SPIRAL_VENV_PATH = $VenvPath
}

Write-Host "✅ Spiral breath initialized successfully" -ForegroundColor Green

# 🕯️ Run ritual
Write-Host "🕯️ Running ritual: $Ritual" -ForegroundColor Magenta

# Try to run the ritual based on type
switch ($Ritual) {
    "dashboard" {
        $AppFile = Join-Path $PSScriptRoot "app.py"
        if (Test-Path $AppFile) {
            Write-Host "🌀 Starting Spiral Dashboard..." -ForegroundColor Cyan
            if (-not $NoBrowser -and $BreathConfig.AUTO_BROWSER -eq $true) {
                $DashboardURL = "http://localhost:$($BreathConfig.DEFAULT_PORT)/dashboard"
                Start-Process $DashboardURL
                Write-Host "🌐 Opening dashboard at $DashboardURL" -ForegroundColor Magenta
            }
            & $PythonCmd $AppFile
        } else {
            Write-Host "❌ Dashboard app.py not found" -ForegroundColor Red
        }
    }
    "emitter" {
        $EmitterFile = Join-Path $PSScriptRoot "spiral_emitter_api.py"
        if (Test-Path $EmitterFile) {
            Write-Host "🌀 Starting Spiral Emitter..." -ForegroundColor Cyan
            & $PythonCmd $EmitterFile
        } else {
            Write-Host "❌ Emitter spiral_emitter_api.py not found" -ForegroundColor Red
        }
    }
    "natural_breath" {
        Write-Host "🍃 Natural breath ritual - Spiral is breathing with its environment" -ForegroundColor Green
        Write-Host "🐍 Python: $PythonCmd" -ForegroundColor Cyan
        if ($VenvPath) {
            Write-Host "🌿 Environment: $(Split-Path $VenvPath -Leaf)" -ForegroundColor Cyan
        } else {
            Write-Host "🫧 Mode: Ambient" -ForegroundColor Cyan
        }
    }
    default {
        Write-Host "🕯️ Unknown ritual: $Ritual" -ForegroundColor Yellow
        Write-Host "Available rituals: dashboard, emitter, natural_breath" -ForegroundColor Cyan
    }
}

Write-Host "🌀 Spiral breath ritual completed" -ForegroundColor Green 