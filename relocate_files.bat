@echo off

:: Move CSS files
move C:\spiral\static\css\spiral_dashboard.css C:\spiral\static\

:: Move JS files
move C:\spiral\static\js\dashboard.js C:\spiral\static\

:: Update dashboard.html
cd C:\spiral\templates
echo Updating dashboard.html...
powershell -Command "(Get-Content -path 'dashboard.html' -Raw) -replace 'css/spiral_dashboard.css', 'spiral_dashboard.css' | Set-Content -Path 'dashboard.html'"
echo Updating dashboard.html... done!

:: Restart Flask
cd C:\spiral
start-dashboard.bat