@echo off
echo ====================================
echo   啟動 Financial News Search 前端
echo ====================================
echo.

cd /d "%~dp0"

echo 正在檢查依賴...
if not exist "node_modules" (
    echo 首次啟動，正在安裝依賴...
    call npm install
)

echo.
echo 正在啟動開發伺服器...
echo 伺服器啟動後會自動開啟瀏覽器
echo.
echo 按 Ctrl+C 可以停止伺服器
echo.

REM 等待一下讓伺服器啟動，然後開啟瀏覽器
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5173"

call npm run dev

pause
