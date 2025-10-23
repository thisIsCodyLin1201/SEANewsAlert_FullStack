@echo off
chcp 65001 > nul

REM Change to project root directory
cd /d "%~dp0\.."

echo ====================================
echo   FastAPI Server Startup
echo ====================================
echo.

echo [1/2] Installing packages...
python -m pip install -r requirements-api.txt -q

echo [2/2] Starting FastAPI server...
echo.
echo Server will start at: http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
