@echo off
echo ================================================================
echo    SecureCart Marketplace - Quick Start
echo ================================================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/3] Starting SecureCart Marketplace...
echo.
echo ================================================================
echo Server will start on: http://localhost:5000
echo.
echo IMPORTANT: Make sure MySQL is running!
echo Update MySQL password in app.py before first run
echo ================================================================
echo.

python app.py

pause
