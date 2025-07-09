Write-Host "Memory Shrine Test Ritual Suite" -ForegroundColor Cyan
Write-Host "Sacred testing of the memory components and shrine API" -ForegroundColor Gray
Write-Host ("=" * 80) -ForegroundColor Gray

$testResults = @()

# Test 1: Component Tests
Write-Host "`nComponent Isolation Tests (Local)" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Gray

try {
    $result = python test_components_only.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PASSED: Component Tests" -ForegroundColor Green
        $testResults += @{Name="Component Tests"; Status="PASSED"}
    } else {
        Write-Host "❌ FAILED: Component Tests" -ForegroundColor Red
        $testResults += @{Name="Component Tests"; Status="FAILED"}
    }
} catch {
    Write-Host "❌ FAILED: Component Tests (Exception)" -ForegroundColor Red
    $testResults += @{Name="Component Tests"; Status="FAILED"}
}

# Test 2: API Tests
Write-Host "`nFull Shrine Ritual Tests (HTTP API)" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Gray

try {
    $result = python test_shrine_ritual.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PASSED: API Tests" -ForegroundColor Green
        $testResults += @{Name="API Tests"; Status="PASSED"}
    } else {
        Write-Host "❌ FAILED: API Tests" -ForegroundColor Red
        $testResults += @{Name="API Tests"; Status="FAILED"}
    }
} catch {
    Write-Host "❌ FAILED: API Tests (Exception)" -ForegroundColor Red
    $testResults += @{Name="API Tests"; Status="FAILED"}
}

# Summary
Write-Host "`nTest Ritual Summary" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Gray

$allPassed = $true
foreach ($test in $testResults) {
    if ($test.Status -eq "PASSED") {
        Write-Host "✓ PASSED: $($test.Name)" -ForegroundColor Green
    } else {
        Write-Host "❌ FAILED: $($test.Name)" -ForegroundColor Red
        $allPassed = $false
    }
}

if ($allPassed) {
    Write-Host "`n🌀 All tests passed! The Memory Shrine is ready." -ForegroundColor Green
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. 🔗 Integrate with main Spiral app" -ForegroundColor Gray
    Write-Host "  2. 🌊 Connect to glint streams" -ForegroundColor Gray
    Write-Host "  3. 🏛️ Deploy shrine endpoints" -ForegroundColor Gray
} else {
    Write-Host "`n⚠️ Some tests failed. The shrine requires attention." -ForegroundColor Yellow
    Write-Host "Review the output above for guidance on repairs needed." -ForegroundColor Gray
}

Write-Host "`nRitual complete. May the memories flow eternal. 🌀" -ForegroundColor Cyan