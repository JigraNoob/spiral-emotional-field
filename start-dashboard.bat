@echo off
setlocal ENABLEDELAYEDEXPANSION

:: 🌿 Spiral Dashboard Launch Ritual
echo [≡] Spiral Breathline initializing from C:\spiral...
set PROJECT_DIR=C:\spiral
set VENV_DIR=%PROJECT_DIR%\swe-1
set FLASK_APP=app.py
set PORT=5000
set PYTHONPATH=%PROJECT_DIR%

:: 🧪 Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [✘] Virtual environment not found at %VENV_DIR%
    echo [→] Create it first with: python -m venv swe-1
    pause
    exit /b 1
)

:: 🌬 Activate the breathline
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [✘] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [✓] Virtual environment activated: swe-1

:: 🧩 Check for required packages
python --version
pip show flask >nul 2>&1 || echo [!] Flask is not installed.
pip show flask_socketio >nul 2>&1 || echo [!] flask_socketio is missing.

:: 🚪 Move into project directory
cd /d %PROJECT_DIR%
echo [⇡] Entering Spiral chamber...

:: 🔁 Set PYTHONPATH for import resolution
set PYTHONPATH=%PROJECT_DIR%

:: 🔥 Launch Spiral Dashboard (Flask)
echo [🌀] Spiral Dashboard breathing on port %PORT%...
python app.py
if errorlevel 1 (
    echo [✘] Spiral Dashboard failed to start. Check logs above.
    pause
    exit /b 1
)

:: 🌐 Final output
echo [✓] Visit: http://localhost:%PORT%/dashboard
endlocal
pause
