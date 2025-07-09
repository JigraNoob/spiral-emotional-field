Write-Host "🏛️ Memory Shrine Test Ritual" -ForegroundColor Cyan
Write-Host "=" * 50

# Test 1: Component isolation
Write-Host "`n1. Testing components in isolation..." -ForegroundColor Yellow
python test_components_only.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Component tests failed" -ForegroundColor Red
    exit 1
}

# Test 2: Full shrine ritual (if memory shrine app is running)
Write-Host "`n2. Testing full shrine ritual..." -ForegroundColor Yellow
$shrineRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5100/" -TimeoutSec 5 -ErrorAction Stop
    $shrineRunning = $true
} catch {
    Write-Host "⚠️ Memory Shrine app not running on localhost:5100" -ForegroundColor Yellow
    Write-Host "   Skipping API tests. To run full tests:" -ForegroundColor Gray
    Write-Host "   1. Start the Memory Shrine: python -m apps.memory_shrine.app" -ForegroundColor Gray
    Write-Host "   2. Then run: python test_shrine_ritual.py" -ForegroundColor Gray
}

if ($shrineRunning) {
    python test_shrine_ritual.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Shrine ritual tests failed" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n🌀 Memory Shrine tests complete!" -ForegroundColor Green
Write-Host "The shrine breathes and remembers." -ForegroundColor Cyan