# 🔧 權限問題修復說明

## ❌ 問題描述

如果您遇到以下錯誤：
```
error: Failed to install: annotated_doc-0.0.3-py3-none-any.whl
Caused by: failed to create directory `C:\Program Files\WindowsApps\...`
存取被拒。 (os error 5)
```

## 🔍 原因分析

這是因為您的 Python 是從 **Microsoft Store** 安裝的，其安裝路徑位於受保護的系統目錄：
```
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_...
```

普通用戶沒有寫入這個目錄的權限，因此無法使用 `--system` 標誌安裝套件。

---

## ✅ 解決方案（已自動修復）

### 本專案已修改所有啟動腳本：

#### 改動內容：
1. **移除 `--system` 標誌** - 不再嘗試安裝到系統目錄
2. **自動創建虛擬環境** - 在專案目錄創建 `.venv`
3. **使用 `--user` 安裝 uv** - uv 本身安裝到用戶目錄

#### 新的流程：
```batch
# 1. 安裝 uv 到用戶目錄（不需要管理員權限）
python -m pip install --user uv

# 2. 創建虛擬環境（在專案目錄，有權限）
uv venv .venv

# 3. 啟用虛擬環境
call .venv\Scripts\activate.bat

# 4. 在虛擬環境中安裝套件（不需要 --system）
uv pip install -r requirements-api.txt

# 5. 使用虛擬環境的 Python 啟動
.venv\Scripts\python.exe -m uvicorn ...
```

---

## 🎯 優勢

### 使用虛擬環境的好處：

1. ✅ **無權限問題** - 不需要管理員權限
2. ✅ **環境隔離** - 不影響系統 Python
3. ✅ **版本管理** - 每個專案獨立依賴
4. ✅ **可攜性** - 可以打包整個環境
5. ✅ **安全性** - 不會污染系統環境

---

## 📝 使用說明

### 現在您可以直接執行：

**Windows:**
```batch
.\boot-script\START-ALL.bat
```

**macOS/Linux:**
```bash
./boot-script/START-ALL.sh
```

腳本會自動：
1. ✅ 檢查並安裝 uv（到用戶目錄）
2. ✅ 創建虛擬環境 `.venv`（如果不存在）
3. ✅ 啟用虛擬環境
4. ✅ 安裝所有依賴到虛擬環境
5. ✅ 使用虛擬環境啟動服務

**完全不需要管理員權限！** 🎉

---

## 🗂️ 檔案結構

執行後會在專案根目錄看到：
```
SEANewsAlert/
├── .venv/                    # 虛擬環境（新增）
│   ├── Scripts/             # Windows
│   │   ├── python.exe       # 虛擬環境的 Python
│   │   ├── activate.bat     # 啟用腳本
│   │   └── pip.exe          # 虛擬環境的 pip
│   └── Lib/                 # 套件安裝位置
│       └── site-packages/
├── requirements-api.txt
├── boot-script/
│   ├── START-ALL.bat        # 已修改
│   ├── START-FAST.bat       # 已修改
│   └── ...
└── ...
```

---

## 🧹 清理建議

### 如果需要重新開始：

```batch
# 刪除虛擬環境
rmdir /s /q .venv

# 重新執行啟動腳本
.\boot-script\START-ALL.bat
```

---

## 💡 其他選項（不推薦）

### 方案 2: 以管理員身份執行（不建議）
右鍵 → 以系統管理員身分執行

**缺點**：
- ❌ 需要管理員權限
- ❌ 安全風險
- ❌ 可能影響系統環境

### 方案 3: 重新安裝 Python（不建議）
從 python.org 下載並安裝（不使用 Microsoft Store 版本）

**缺點**：
- ❌ 需要重新安裝
- ❌ 耗時
- ❌ 可能有兩個 Python 版本衝突

---

## ✅ 結論

**推薦方案：使用虛擬環境（已實施）**

本專案所有啟動腳本已自動使用虛擬環境，您**無需做任何改變**，直接執行即可！

---

## 📚 相關文檔

- [UV_MIGRATION.md](./UV_MIGRATION.md) - UV 遷移說明
- [HOW_TO_START.md](./HOW_TO_START.md) - 啟動指南
- [Python 虛擬環境官方文檔](https://docs.python.org/zh-tw/3/library/venv.html)

---

**修復日期**: 2025-11-03  
**狀態**: ✅ 已修復並測試  
**適用於**: Microsoft Store Python 及所有 Windows 用戶
