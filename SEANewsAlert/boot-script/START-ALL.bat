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
echo.

REM 使用 requirements-api.txt 安裝所有套件
python -m pip install --upgrade pip -q
python -m pip install -r requirements-api.txt -q

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

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
