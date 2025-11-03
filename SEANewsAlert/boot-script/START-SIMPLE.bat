@echo off
chcp 65001 > nul

REM Change to project root directory
cd /d "%~dp0\.."

echo ====================================
echo   FastAPI Server Startup
echo ====================================
echo.

echo [1/2] Installing packages...

REM 檢查並安裝 uv
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo     正在安裝 uv 套件管理器...
    python -m pip install --user uv -q
)

REM 檢查並創建虛擬環境
if not exist ".venv" (
    echo     正在創建虛擬環境...
    uv venv .venv
)

REM 啟用虛擬環境並安裝
call .venv\Scripts\activate.bat
uv pip install -r requirements-api.txt

echo [2/2] Starting FastAPI server...
echo.
echo Server will start at: http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
