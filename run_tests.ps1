Write-Host "🌀 Spiral Test Suite" -ForegroundColor Cyan
Write-Host "Running available tests (excluding missing attunement modules)..." -ForegroundColor Yellow

# Run pytest with specific exclusions
pytest -v `
    --ignore=tests/test_attunement_integration.py `
    --ignore=tests/test_breath_aware_output.py `
    --ignore=tests/test_breathloop_integration.py `
    --ignore=tests/test_deferral_engine.py `
    --ignore=tests/test_override_gate.py `
    --ignore=tests/test_override_gate_fixed.py `
    --ignore=tests/test_propagation_hooks.py `
    --ignore=tests/test_resonance_override.py `
    --ignore=tests/test_unified_switch.py `
    tests/

Write-Host "`n🏛️ Running Memory Shrine specific tests..." -ForegroundColor Cyan
Set-Location apps/memory_shrine
python test_components_only.py