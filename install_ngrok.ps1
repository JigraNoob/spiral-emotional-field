# Install ngrok for Windows
Write-Host "Installing ngrok..." -ForegroundColor Green

# Create temp directory
$tempDir = "$env:TEMP\ngrok_install"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

# Download ngrok
Write-Host "Downloading ngrok..." -ForegroundColor Yellow
$ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
$zipPath = "$tempDir\ngrok.zip"
$extractPath = "$tempDir\ngrok"

try {
    Invoke-WebRequest -Uri $ngrokUrl -OutFile $zipPath
    Write-Host "Download complete" -ForegroundColor Green
} catch {
    Write-Host "Download failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Extract ngrok
Write-Host "Extracting ngrok..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
    Write-Host "Extraction complete" -ForegroundColor Green
} catch {
    Write-Host "Extraction failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Copy to a directory in PATH
$installDir = "$env:USERPROFILE\ngrok"
New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Copy-Item "$extractPath\ngrok.exe" -Destination "$installDir\ngrok.exe" -Force

# Add to PATH if not already there
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$installDir", "User")
    Write-Host "Added ngrok to PATH" -ForegroundColor Green
} else {
    Write-Host "ngrok already in PATH" -ForegroundColor Green
}

# Clean up
Remove-Item $tempDir -Recurse -Force

Write-Host "ngrok installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Close and reopen your terminal/PowerShell" -ForegroundColor White
Write-Host "2. Run: ngrok config add-authtoken <your_token>" -ForegroundColor White
Write-Host "3. Get your token from: https://dashboard.ngrok.com" -ForegroundColor White
Write-Host ""
Write-Host "Then you can run: python ritual_ngrok_shrine.py" -ForegroundColor White 