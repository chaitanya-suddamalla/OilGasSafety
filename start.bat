@echo off
REM Oil & Gas Safety Bot - Startup Script

echo.
echo ============================================================
echo Oil & Gas Plant Safety Bot - Starting
echo ============================================================
echo.

REM Check if Python is available
"C:\ProgramData\Anaconda3\python.exe" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please ensure Anaconda is installed.
    pause
    exit /b 1
)

echo Installing/updating dependencies...
"C:\ProgramData\Anaconda3\python.exe" -m pip install --upgrade pip setuptools wheel >nul 2>&1

echo.
echo ============================================================
echo Starting Flask Server...
echo ============================================================
echo.
echo Server will start on: http://localhost:5000
echo Open your browser and visit: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

"C:\ProgramData\Anaconda3\python.exe" server.py

pause
