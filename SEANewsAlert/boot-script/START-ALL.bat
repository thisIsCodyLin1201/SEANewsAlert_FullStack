@echo off
chcp 65001 > nul

REM 切換到專案根目錄（.bat 檔案的上一層）
cd /d "%~dp0\.."

echo ========================================
echo 🚀 一鍵安裝所有依賴並啟動
echo ========================================
echo.
echo 📂 工作目錄: %CD%
echo.

echo [1/2] 安裝所有必要套件...
echo     這可能需要 1-2 分鐘，請稍候...
echo     使用 uv 進行快速安裝...
echo.

REM 檢查 uv 是否安裝
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 未找到 uv，正在安裝...
    python -m pip install --user uv -q
)

REM 檢查是否存在虛擬環境，如果不存在則創建
if not exist ".venv" (
    echo     正在創建虛擬環境...
    uv venv .venv
)

REM 啟用虛擬環境並安裝套件
call .venv\Scripts\activate.bat
uv pip install -r requirements-api.txt

if %errorlevel% neq 0 (
    echo [錯誤] 套件安裝失敗
    echo 請檢查 requirements-api.txt 是否存在
    pause
    exit /b 1
)

echo     ✅ 套件安裝完成
echo.

echo [2/2] 啟動 FastAPI 服務...
echo.
echo ========================================
echo 🎉 服務啟動成功！
echo ========================================
echo 📚 API 文檔:   http://127.0.0.1:8000/docs
echo 🌐 測試前端:   http://127.0.0.1:8000/static/index.html
echo ❤️  健康檢查:   http://127.0.0.1:8000/health
echo ========================================
echo 按 Ctrl+C 停止服務
echo ========================================
echo.

REM 確保使用虛擬環境的 Python
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
