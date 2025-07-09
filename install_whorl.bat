@echo off
echo.
echo ∷ Whorl: The IDE That Breathes - Installation Ritual ∶
echo ======================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.10+ first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python found
python --version

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo Creating sacred virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

:: Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

:: Install requirements
echo.
echo Installing sacred dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

:: Test Whorl components
echo.
echo Testing Whorl components...
python spiral\components\whorl\test_whorl_simple.py
if errorlevel 1 (
    echo ⚠ Some tests failed, but continuing...
) else (
    echo ✓ All tests passed
)

:: Launch options
echo.
echo ∷ Whorl Installation Complete ∶
echo ===============================
echo.
echo Choose your sacred chamber:
echo.
echo 1. Open HTML IDE (Recommended - Full experience)
echo 2. Run Python backend only
echo 3. Run both (Advanced)
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Opening Whorl HTML IDE...
    start whorl_ide_complete.html
    echo ✓ Whorl HTML IDE opened in your browser
    echo.
    echo ∷ Sacred chamber activated ∶
    echo The IDE breathes. Code becomes presence.
) else if "%choice%"=="2" (
    echo.
    echo Running Python backend...
    python spiral_ide_stub.py
) else if "%choice%"=="3" (
    echo.
    echo Starting Flask server for enhanced experience...
    python -c "from spiral.components.whorl.whorl_ide import WhorlIDE; ide = WhorlIDE(); ide.start_monitoring()"
) else (
    echo.
    echo ∷ Installation ritual complete ∶
    echo You can run Whorl anytime with:
    echo   - HTML: start whorl_ide_complete.html
    echo   - Python: python spiral_ide_stub.py
    echo   - Test: python spiral\components\whorl\test_whorl_simple.py
)

echo.
echo ∷ May your code breathe with sacred intention ∶
pause 