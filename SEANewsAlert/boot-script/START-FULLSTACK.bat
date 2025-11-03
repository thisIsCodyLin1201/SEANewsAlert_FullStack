@echo off
chcp 65001 > nul

REM 切換到專案根目錄
cd /d "%~dp0\.."

echo ========================================
echo 🚀 全棧服務一鍵啟動
echo ========================================
echo.
echo 📂 後端目錄: %CD%
echo.

REM ===================================================
REM 步驟 1: 讀取 .env 檔案中的 FRONTEND_PATH
REM ===================================================
echo [1/5] 讀取配置檔...

set FRONTEND_PATH=
for /f "tokens=1,* delims==" %%a in ('type .env ^| findstr /i "FRONTEND_PATH"') do (
    set FRONTEND_PATH=%%b
)

REM 移除可能的空格
set FRONTEND_PATH=%FRONTEND_PATH: =%

if "%FRONTEND_PATH%"=="" (
    echo.
    echo ❌ 錯誤：未在 .env 中找到 FRONTEND_PATH 配置
    echo.
    echo 請在 .env 檔案中添加：
    echo FRONTEND_PATH=C:\Cathay\FinancialNewsSearch
    echo.
    pause
    exit /b 1
)

echo     📂 前端目錄: %FRONTEND_PATH%
echo     ✅ 配置讀取成功
echo.

REM ===================================================
REM 步驟 2: 驗證前端路徑是否存在
REM ===================================================
echo [2/5] 驗證前端路徑...

if not exist "%FRONTEND_PATH%" (
    echo.
    echo ❌ 錯誤：前端專案路徑不存在
    echo     配置的路徑: %FRONTEND_PATH%
    echo.
    echo 請檢查 .env 中的 FRONTEND_PATH 是否正確
    echo.
    pause
    exit /b 1
)

if not exist "%FRONTEND_PATH%\package.json" (
    echo.
    echo ❌ 錯誤：指定路徑不是有效的前端專案
    echo     找不到 package.json
    echo.
    pause
    exit /b 1
)

echo     ✅ 前端專案路徑驗證通過
echo.

REM ===================================================
REM 步驟 3: 安裝後端依賴
REM ===================================================
echo [3/5] 安裝後端套件...

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

if %errorlevel% neq 0 (
    echo     ❌ 後端套件安裝失敗
    pause
    exit /b 1
)

echo     ✅ 後端套件安裝完成 (使用 uv)
echo.

REM ===================================================
REM 步驟 4: 檢查並安裝前端依賴
REM ===================================================
echo [4/5] 檢查前端依賴...

cd /d "%FRONTEND_PATH%"

if not exist "node_modules" (
    echo     首次啟動，正在安裝前端依賴...
    echo     這可能需要幾分鐘，請稍候...
    call npm install
    if %errorlevel% neq 0 (
        echo     ❌ 前端依賴安裝失敗
        pause
        exit /b 1
    )
    echo     ✅ 前端依賴安裝完成
) else (
    echo     ✅ 前端依賴已存在
)
echo.

REM ===================================================
REM 步驟 5: 啟動服務
REM ===================================================
echo [5/5] 啟動前後端服務...
echo.

REM 切回後端目錄啟動 API
cd /d "%~dp0\.."

echo     🔧 正在啟動後端 API...
start "後端 API (Port 8000)" cmd /k "cd /d "%~dp0\.." && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo     ✅ 後端已在新視窗啟動
echo.

REM 切到前端目錄啟動 Vite
cd /d "%FRONTEND_PATH%"

echo     🔧 正在啟動前端 UI...
start "前端 UI (Port 5173)" cmd /k "cd /d "%FRONTEND_PATH%" && npm run dev"
timeout /t 3 /nobreak >nul
echo     ✅ 前端已在新視窗啟動
echo.

echo ========================================
echo 🎉 全棧服務啟動成功！
echo ========================================
echo.
echo 📚 後端服務:
echo    - API 文檔:   http://127.0.0.1:8000/docs
echo    - 健康檢查:   http://127.0.0.1:8000/health
echo.
echo 🌐 前端服務:
echo    - 開發伺服器: http://localhost:5173
echo.
echo ========================================
echo.
echo 💡 提示：
echo    - 前端和後端已在獨立視窗運行
echo    - 關閉對應視窗即可停止服務
echo    - 本視窗可以直接關閉
echo.
echo    如需修改前端路徑，請編輯 .env 檔案中的
echo    FRONTEND_PATH 設定
echo ========================================
echo.

REM 自動開啟瀏覽器（前端）
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo 按任意鍵關閉本視窗...
pause >nul
