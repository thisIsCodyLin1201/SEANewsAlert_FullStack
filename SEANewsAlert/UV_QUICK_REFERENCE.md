# 🚀 UV 快速參考指南

> **專案已升級至 UV 套件管理器** - 速度提升 10-100 倍！

---

## ⚡ 一鍵啟動（推薦）

### Windows
```batch
# 直接執行，會自動安裝 uv 並啟動
.\boot-script\START-ALL.bat
```

### macOS / Linux
```bash
# 直接執行，會自動安裝 uv 並啟動
./boot-script/START-ALL.sh
```

---

## 📦 常用指令

### 安裝套件
```bash
# 從 requirements.txt 安裝
uv pip install -r requirements-api.txt --system

# 安裝單一套件
uv pip install fastapi --system

# 在虛擬環境中安裝（已啟用 .venv）
uv pip install fastapi
```

### 建立虛擬環境
```bash
# 使用 uv 建立（更快）
uv venv .venv

# 啟用虛擬環境
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 其他操作
```bash
# 列出已安裝套件
uv pip list --system

# 升級套件
uv pip install --upgrade package_name --system

# 移除套件
uv pip uninstall package_name --system

# 清理快取
uv cache clean
```

---

## 🔧 首次安裝 UV

### 方法 1: 使用 pip（推薦）
```bash
pip install uv
```

### 方法 2: 官方安裝腳本

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 💡 提示

- ✅ **自動處理**: 所有啟動腳本會自動檢查並安裝 uv
- ✅ **無需改變**: 用戶無需改變任何使用習慣
- ✅ **完全兼容**: 所有 pip 功能完全支援
- ⚡ **極速安裝**: 比 pip 快 10-100 倍

---

## 📚 更多資訊

- 📖 [UV_MIGRATION.md](./UV_MIGRATION.md) - 完整遷移文檔
- 📋 [MIGRATION_SUMMARY.md](./MIGRATION_SUMMARY.md) - 變更摘要
- 🚀 [HOW_TO_START.md](./HOW_TO_START.md) - 啟動指南
- 🌐 [UV 官方文檔](https://docs.astral.sh/uv/)

---

## ❓ 常見問題

### Q: 需要手動安裝 uv 嗎？
**A:** 不需要！啟動腳本會自動檢查並安裝。

### Q: 會影響現有套件嗎？
**A:** 不會！uv 完全兼容 pip，不會影響已安裝的套件。

### Q: 速度真的快很多嗎？
**A:** 是的！實測快 10-100 倍，特別是在有快取的情況下。

### Q: 可以回退到 pip 嗎？
**A:** 可以！只需將腳本中的 `uv pip` 改回 `python -m pip` 即可。

---

**更新日期**: 2025-11-03  
**狀態**: ✅ 生產就緒
