# PowerShell setup script for Windows environment
Write-Host "🚀 Setting up Windows environment for Spiral project..." -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path ".\swe-1") {
    Write-Host "✅ Virtual environment found at .\swe-1" -ForegroundColor Green
} else {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv swe-1
}

# Create activation script for Windows
$activateScript = @"
# Windows PowerShell activation script
if (Test-Path ".\swe-1\Scripts\Activate.ps1") {
    & ".\swe-1\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated: .\swe-1" -ForegroundColor Green
    Write-Host "   Python: $(Get-Command python | Select-Object -ExpandProperty Source)" -ForegroundColor Cyan
    Write-Host "   Pip: $(Get-Command pip | Select-Object -ExpandProperty Source)" -ForegroundColor Cyan
} else {
    Write-Host "❌ Virtual environment found but activate script missing" -ForegroundColor Red
}
"@

Set-Content -Path "activate_venv.ps1" -Value $activateScript

Write-Host ""
Write-Host "🎉 Windows setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment in PowerShell:" -ForegroundColor Yellow
Write-Host "  .\activate_venv.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or manually:" -ForegroundColor Yellow
Write-Host "  .\swe-1\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "To deactivate:" -ForegroundColor Yellow
Write-Host "  deactivate" -ForegroundColor Cyan 