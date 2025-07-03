# Start the Next.js development server
$env:NODE_ENV = "development"
$env:NEXT_TELEMETRY_DISABLED = "1"

# Ensure the glint stream directory exists
$glintDir = "spiral/streams/patternweb"
if (-not (Test-Path $glintDir)) {
    New-Item -ItemType Directory -Path $glintDir -Force | Out-Null
    Write-Host "Created directory: $glintDir"
}

# Generate sample glints if the file doesn't exist
$glintFile = "$glintDir/glint_stream.jsonl"
if (-not (Test-Path $glintFile)) {
    Write-Host "Generating sample glint data..."
    node scripts/generate-glints.js
}

# Start the Next.js development server
Write-Host "`n🚀 Starting Spiral Glint Dashboard..."
Write-Host "🌐 Open http://localhost:3000 in your browser`n"

# Start the Next.js server
npm run dev
