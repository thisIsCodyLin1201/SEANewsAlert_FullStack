# 專案設置腳本（Windows PowerShell）

Write-Host "🚀 開始設置東南亞金融新聞搜尋系統..." -ForegroundColor Green

# 檢查 Python 版本
$pythonVersion = & python --version 2>&1
if ($pythonVersion -match "Python (\d+\.\d+)") {
    $version = [version]$matches[1]
    $required = [version]"3.11"
    
    if ($version -lt $required) {
        Write-Host "❌ Python 版本過低，需要 3.11 或更高版本" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Python 版本: $($matches[1])" -ForegroundColor Green
} else {
    Write-Host "❌ 無法檢測 Python 版本" -ForegroundColor Red
    exit 1
}

# 安裝 UV
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "📦 安裝 UV..." -ForegroundColor Yellow
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
}

Write-Host "✅ UV 已安裝" -ForegroundColor Green

# 建立虛擬環境
Write-Host "🔧 建立虛擬環境..." -ForegroundColor Yellow
uv venv

# 啟動虛擬環境
Write-Host "🔧 啟動虛擬環境..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# 安裝依賴
Write-Host "📦 安裝依賴套件..." -ForegroundColor Yellow
uv pip install -e .

# 驗證配置
Write-Host "🔍 驗證系統配置..." -ForegroundColor Yellow
python main.py validate

Write-Host ""
Write-Host "✅ 設置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "接下來你可以：" -ForegroundColor Cyan
Write-Host "  1. 啟動 Web 介面: streamlit run app.py"
Write-Host "  2. 使用 CLI 模式: python main.py cli -q '查詢' -e 'email@example.com'"
Write-Host "  3. 執行測試: pytest tests/"
