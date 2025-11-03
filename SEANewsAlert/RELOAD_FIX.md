# 🔧 無限重載問題修復

## ❌ 問題描述

啟動服務後出現無限重載循環：
```
WARNING:  WatchFiles detected changes in '.venv\Lib\site-packages\...'
Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
...
```

## 🔍 原因分析

`uvicorn --reload` 模式會監控所有 Python 檔案變化，包括：
- ✅ 你的專案代碼（應該監控）
- ❌ `.venv` 虛擬環境中的套件（不應該監控）

當虛擬環境中的套件文件被觸碰或修改時，會觸發重載，導致無限循環。

---

## ✅ 解決方案（已自動修復）

### 已修改所有啟動腳本：

改用 `--reload-dir` 參數，只監控特定目錄，而不是排除 `.venv`：

**修改前：**
```batch
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**修改後（使用白名單方式）：**
```batch
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir app --reload-dir agents --reload-dir utils
```

**為什麼改用 `--reload-dir`？**
- ✅ 避免 Windows 萬用字元展開問題
- ✅ 白名單方式更精確控制
- ✅ 只監控專案代碼目錄
- ✅ 完全避免 `.venv` 被監控

---

## 📋 已修改的檔案

### Windows 批次腳本 (.bat)
1. ✅ `START-ALL.bat`
2. ✅ `START-FAST.bat`
3. ✅ `START-SIMPLE.bat`
4. ✅ `START-FULLSTACK.bat`
5. ✅ `START-FULLSTACK-SIMPLE.bat`

### Linux/macOS Shell 腳本 (.sh)
6. ✅ `START-ALL.sh`
7. ✅ `START-FAST.sh`

---

## 🎯 效果

### 修復前：
```
✅ 系統啟動
⚠️  檢測到 .venv 變化 → 重載
✅ 系統啟動
⚠️  檢測到 .venv 變化 → 重載
✅ 系統啟動
⚠️  檢測到 .venv 變化 → 重載
... (無限循環)
```

### 修復後：
```
✅ 系統啟動
✅ 運行中... (穩定)
✅ 偵測到你的代碼變化 → 重載 (正常)
✅ 運行中... (穩定)
```

---

## 📝 `--reload-dir` 參數說明

```bash
--reload-dir app --reload-dir agents --reload-dir utils
```

| 參數 | 說明 |
|------|------|
| `--reload` | 啟用自動重載模式 |
| `--reload-dir` | 指定要監控的目錄（白名單） |
| `app` | 監控 app 目錄（FastAPI 路由） |
| `agents` | 監控 agents 目錄（AI Agents） |
| `utils` | 監控 utils 目錄（工具函數） |

**優勢**：只監控需要的目錄，完全忽略其他所有目錄（包括 `.venv`、`reports`、`__pycache__` 等）

---

## 🔍 如何添加更多監控目錄

如果未來有新的代碼目錄需要監控，可以添加更多 `--reload-dir`：

```batch
python -m uvicorn app.main:app \
  --reload \
  --reload-dir app \
  --reload-dir agents \
  --reload-dir utils \
  --reload-dir services \
  --reload-dir models
```

**注意**：只有明確指定的目錄會被監控，其他所有目錄（`.venv`、`reports`、`tests` 等）都會被自動忽略。

---

## 🚀 現在可以正常使用

直接執行啟動腳本，不會再有無限重載問題：

**Windows:**
```batch
.\boot-script\START-ALL.bat
```

**macOS/Linux:**
```bash
./boot-script/START-ALL.sh
```

系統會正常啟動並穩定運行，只在你修改專案代碼時才會重載。

---

## 💡 開發建議

### 何時會觸發重載（正常）：
- ✅ 修改 Python 源代碼 (`.py`)
- ✅ 修改配置文件 (如果被監控)
- ✅ 新增/刪除 Python 文件

### 何時不會觸發重載（預期行為）：
- ✅ `.venv` 目錄變化
- ✅ `reports/` 目錄變化
- ✅ 日誌文件變化
- ✅ `__pycache__` 變化

---

## 🔧 手動啟動參數

如果需要手動啟動並自定義監控目錄：

```bash
# Windows
.venv\Scripts\python.exe -m uvicorn app.main:app ^
  --host 127.0.0.1 ^
  --port 8000 ^
  --reload ^
  --reload-dir app ^
  --reload-dir agents ^
  --reload-dir utils

# macOS/Linux
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload \
  --reload-dir app \
  --reload-dir agents \
  --reload-dir utils
```

---

## 📚 相關文檔

- [Uvicorn Reload 文檔](https://www.uvicorn.org/#command-line-options)
- [Watchfiles 文檔](https://watchfiles.helpmanual.io/)

---

**修復日期**: 2025-11-03  
**狀態**: ✅ 已修復並測試  
**影響**: 所有啟動腳本，無限重載問題已解決
