@echo off
chcp 65001 > nul

REM Change to project root directory
cd /d "%~dp0\.."

echo ========================================
echo   Full-Stack Server Startup
echo ========================================
echo.

REM ===================================================
REM Step 1: Read FRONTEND_PATH from .env
REM ===================================================
echo [1/5] Reading configuration...

set FRONTEND_PATH=
for /f "tokens=1,* delims==" %%a in ('type .env ^| findstr /i "FRONTEND_PATH"') do (
    set FRONTEND_PATH=%%b
)

REM Remove spaces
set FRONTEND_PATH=%FRONTEND_PATH: =%

if "%FRONTEND_PATH%"=="" (
    echo.
    echo ERROR: FRONTEND_PATH not found in .env
    echo.
    echo Please add to .env file:
    echo FRONTEND_PATH=C:\Cathay\FinancialNewsSearch
    echo.
    pause
    exit /b 1
)

echo     Frontend path: %FRONTEND_PATH%
echo     Config loaded successfully
echo.

REM ===================================================
REM Step 2: Verify frontend path exists
REM ===================================================
echo [2/5] Verifying frontend path...

if not exist "%FRONTEND_PATH%" (
    echo.
    echo ERROR: Frontend path does not exist
    echo     Path: %FRONTEND_PATH%
    echo.
    pause
    exit /b 1
)

if not exist "%FRONTEND_PATH%\package.json" (
    echo.
    echo ERROR: Not a valid frontend project
    echo     package.json not found
    echo.
    pause
    exit /b 1
)

echo     Frontend project verified
echo.

REM ===================================================
REM Step 3: Install backend dependencies
REM ===================================================
echo [3/5] Installing backend packages...

python -m pip install --upgrade pip -q
python -m pip install -r requirements-api.txt -q

if %errorlevel% neq 0 (
    echo     Backend installation failed
    pause
    exit /b 1
)

echo     Backend packages installed
echo.

REM ===================================================
REM Step 4: Check and install frontend dependencies
REM ===================================================
echo [4/5] Checking frontend dependencies...

cd /d "%FRONTEND_PATH%"

if not exist "node_modules" (
    echo     First time setup, installing dependencies...
    echo     This may take a few minutes...
    call npm install
    if %errorlevel% neq 0 (
        echo     Frontend installation failed
        pause
        exit /b 1
    )
    echo     Frontend dependencies installed
) else (
    echo     Frontend dependencies ready
)
echo.

REM ===================================================
REM Step 5: Start services
REM ===================================================
echo [5/5] Starting services...
echo.

REM Start backend API
cd /d "%~dp0\.."

echo     Starting backend API...
start "Backend API (Port 8000)" cmd /k "cd /d "%~dp0\.." && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo     Backend started in new window
echo.

REM Start frontend Vite
cd /d "%FRONTEND_PATH%"

echo     Starting frontend UI...
start "Frontend UI (Port 5173)" cmd /k "cd /d "%FRONTEND_PATH%" && npm run dev"
timeout /t 3 /nobreak >nul
echo     Frontend started in new window
echo.

echo ========================================
echo   Full-Stack Services Started!
echo ========================================
echo.
echo Backend Services:
echo    - API Docs:      http://127.0.0.1:8000/docs
echo    - Health Check:  http://127.0.0.1:8000/health
echo.
echo Frontend Service:
echo    - Dev Server:    http://localhost:5173
echo.
echo ========================================
echo.
echo Tips:
echo    - Frontend and backend are running in separate windows
echo    - Close the windows to stop services
echo    - You can close this window now
echo.
echo    To change frontend path, edit FRONTEND_PATH in .env
echo ========================================
echo.

REM Auto open browser (frontend)
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo Press any key to close this window...
pause >nul
