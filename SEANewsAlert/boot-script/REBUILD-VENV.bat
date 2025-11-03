@echo off
chcp 65001 > nul

REM 切換到專案根目錄（.bat 檔案的上一層）
cd /d "%~dp0\.."

echo ========================================
echo 完全重建虛擬環境
echo ========================================
echo.
echo 📂 工作目錄: %CD%
echo.
echo [警告] 這會刪除現有的 .venv 目錄
echo.
pause

echo [1/3] 刪除舊的虛擬環境...
if exist ".venv" (
    rmdir /s /q .venv
    echo     已刪除
) else (
    echo     不存在舊環境
)

echo [2/3] 創建新的虛擬環境...

REM 檢查並安裝 uv
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo     正在安裝 uv 套件管理器...
    python -m pip install uv -q
)

uv venv .venv
if %errorlevel% neq 0 (
    echo [錯誤] 創建失敗，請檢查 Python 安裝
    pause
    exit /b 1
)
echo     創建成功 (使用 uv)

echo [3/3] 安裝基礎套件...
uv pip install fastapi uvicorn[standard] pydantic[email]

echo.
echo ========================================
echo 虛擬環境重建完成！
echo ========================================
echo.
echo 現在請執行: START-API-FIX.bat
echo.
pause
