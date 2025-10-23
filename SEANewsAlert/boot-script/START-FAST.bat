@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM 切換到專案根目錄（.bat 檔案的上一層）
cd /d "%~dp0\.."

echo ========================================
echo 東南亞金融新聞搜尋系統 - 快速啟動
echo ========================================
echo.
echo 📂 工作目錄: %CD%
echo.

REM 檢查 Python 是否安裝
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python，請先安裝 Python 3.11+
    pause
    exit /b 1
)

echo [步驟 1/3] 檢查套件...

REM 直接使用系統 Python 檢查 FastAPI 是否已安裝
python -c "import fastapi" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 FastAPI...
    python -m pip install fastapi -q
)

python -c "import uvicorn" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Uvicorn...
    python -m pip install uvicorn[standard] -q
)

python -c "import pydantic" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Pydantic...
    python -m pip install pydantic[email] -q
)

REM 檢查 ddgs (DuckDuckGo 搜尋)
python -c "import ddgs" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 DuckDuckGo 搜尋工具...
    python -m pip install ddgs -q
)

REM 檢查其他關鍵套件
python -c "import agno" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Agno 框架...
    python -m pip install agno -q
)

python -c "import reportlab" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 ReportLab (PDF 生成)...
    python -m pip install reportlab -q
)

python -c "import pandas" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Pandas (Excel 生成)...
    python -m pip install pandas openpyxl -q
)

echo     套件檢查完成

echo [步驟 2/3] 檢查依賴...
if exist "requirements-api.txt" (
    echo     安裝 API 依賴...
    python -m pip install -r requirements-api.txt -q
)

echo [步驟 3/3] 啟動服務...
echo.
echo ========================================
echo 🚀 服務啟動中...
echo ========================================
echo 📚 API 文檔:   http://127.0.0.1:8000/docs
echo 🌐 測試前端:   http://127.0.0.1:8000/static/index.html
echo ❤️  健康檢查:   http://127.0.0.1:8000/health
echo ========================================
echo 按 Ctrl+C 停止服務
echo ========================================
echo.

REM 使用系統 Python 啟動（不依賴虛擬環境）
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
