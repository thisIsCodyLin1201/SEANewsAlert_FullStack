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

REM 檢查並安裝 uv
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo     正在安裝 uv 套件管理器...
    python -m pip install --user uv -q
    echo     ✅ uv 安裝完成
)

REM 檢查是否存在虛擬環境
if not exist ".venv" (
    echo     正在創建虛擬環境...
    uv venv .venv
)

REM 啟用虛擬環境
call .venv\Scripts\activate.bat

REM 檢查並安裝套件（在虛擬環境中）
python -c "import fastapi" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 FastAPI...
    uv pip install fastapi
)

python -c "import uvicorn" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Uvicorn...
    uv pip install uvicorn[standard]
)

python -c "import pydantic" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Pydantic...
    uv pip install pydantic[email]
)

REM 檢查其他關鍵套件
python -c "import agno" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Agno 框架...
    uv pip install agno
)

python -c "import reportlab" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 ReportLab (PDF 生成)...
    uv pip install reportlab
)

python -c "import pandas" > nul 2>&1
if %errorlevel% neq 0 (
    echo     安裝 Pandas (Excel 生成)...
    uv pip install pandas openpyxl
)

echo     套件檢查完成

echo [步驟 2/3] 檢查依賴...
if exist "requirements-api.txt" (
    echo     安裝 API 依賴...
    uv pip install -r requirements-api.txt
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

REM 使用虛擬環境的 Python 啟動，只監控特定目錄
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir app --reload-dir agents --reload-dir utils
