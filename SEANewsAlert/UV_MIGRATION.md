# 🚀 UV 套件管理器遷移說明

## 📋 概述

本專案已從傳統的 `pip` 遷移至 **[uv](https://github.com/astral-sh/uv)** 套件管理器。

## ✨ 為什麼使用 uv？

- **⚡ 極速安裝**: 比 pip 快 10-100 倍
- **🔒 可靠性**: 更好的依賴解析
- **💾 快取機制**: 智能快取減少重複下載
- **🎯 兼容性**: 完全兼容 pip 和 requirements.txt

## 📦 安裝 uv

### Windows
```bash
# 使用 PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip
python -m pip install uv
```

### macOS / Linux
```bash
# 使用 curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
python -m pip install uv
```

## 🔄 已更新的腳本

所有啟動腳本已自動整合 uv：

### Windows (.bat)
- ✅ `START-ALL.bat` - 完整安裝並啟動
- ✅ `START-FAST.bat` - 快速啟動（檢查套件）
- ✅ `START-SIMPLE.bat` - 簡單啟動
- ✅ `START-FULLSTACK.bat` - 全棧啟動
- ✅ `START-FULLSTACK-SIMPLE.bat` - 全棧簡單啟動
- ✅ `REBUILD-VENV.bat` - 重建虛擬環境

### macOS / Linux (.sh)
- ✅ `START-ALL.sh` - 完整安裝並啟動
- ✅ `START-FAST.sh` - 快速啟動（檢查套件）
- ✅ `REBUILD-VENV.sh` - 重建虛擬環境

## 🎯 自動檢查機制

所有腳本都包含自動檢查邏輯：

```batch
REM 自動檢查並安裝 uv
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安裝 uv 套件管理器...
    python -m pip install uv -q
)
```

**如果系統未安裝 uv，腳本會自動安裝！** 🎉

## 📝 手動使用 uv

### 安裝套件
```bash
# 安裝單一套件（系統級別）
uv pip install fastapi --system

# 從 requirements.txt 安裝
uv pip install -r requirements-api.txt --system

# 在虛擬環境中安裝（如果已啟用 venv）
uv pip install fastapi
```

### 建立虛擬環境
```bash
# 使用 uv 建立虛擬環境（更快）
uv venv .venv

# 啟用虛擬環境
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 升級套件
```bash
# 升級單一套件
uv pip install --upgrade fastapi --system

# 升級所有套件
uv pip install --upgrade -r requirements-api.txt --system
```

## 🔍 常見指令對照

| 功能 | pip | uv |
|------|-----|-----|
| 安裝套件 | `pip install package` | `uv pip install package --system` |
| 安裝 requirements | `pip install -r requirements.txt` | `uv pip install -r requirements.txt --system` |
| 建立虛擬環境 | `python -m venv .venv` | `uv venv .venv` |
| 升級套件 | `pip install --upgrade package` | `uv pip install --upgrade package --system` |
| 列出套件 | `pip list` | `uv pip list --system` |
| 移除套件 | `pip uninstall package` | `uv pip uninstall package --system` |

## ⚠️ 注意事項

1. **--system 標誌**: 在系統 Python 中使用時需要加上 `--system` 標誌
2. **虛擬環境**: 在啟用的虛擬環境中不需要 `--system` 標誌
3. **兼容性**: 完全兼容現有的 requirements.txt 文件

## 🎊 優勢對比

### 速度測試範例
```
安裝 requirements-api.txt (18 個套件):
- pip: ~45 秒
- uv:  ~5 秒

提升: 9x 更快！ 🚀
```

## 📚 更多資源

- [uv 官方文檔](https://docs.astral.sh/uv/)
- [uv GitHub](https://github.com/astral-sh/uv)
- [速度對比測試](https://github.com/astral-sh/uv#benchmarks)

## 🔄 回滾至 pip（如需要）

如果需要暫時回到 pip，只需修改腳本中的：
```batch
uv pip install -r requirements-api.txt --system
```
改回：
```batch
python -m pip install -r requirements-api.txt
```

---

**遷移日期**: 2025-11-03  
**狀態**: ✅ 完成  
**影響範圍**: 所有 Python 套件安裝相關腳本
