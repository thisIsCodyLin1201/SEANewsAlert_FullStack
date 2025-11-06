# 🔧 使用者問題修復指南

## 📋 問題清單與解決方案

### ~~❌ 問題 1: ModuleNotFoundError: No module named 'ddgs'~~ ✅ 已移除

**更新說明：**

專案已改用 **OpenAI Responses API** 進行網路搜尋，不再使用 DuckDuckGo Search (`ddgs`)。

**如果仍看到此錯誤：**
- 可能是使用了舊版本的代碼
- 請確認使用最新版本，已完全移除 `ddgs` 依賴

**技術說明：**
```python
# 舊方式（已移除）
from ddgs import DDGS

# 新方式（OpenAI Responses API）
from openai import OpenAI
client = OpenAI()
# 使用 GPT 模型進行網路搜尋
```

---

### ❌ 問題 2: 'npm' is not recognized as an internal or external command

**錯誤訊息：**
```
'npm' is not recognized as an internal or external command,
operable program or batch file
```

**原因：**
系統未安裝 Node.js，或 npm 未加入系統 PATH。

**解決方案：**

#### 方法 1: 安裝 Node.js（推薦）⭐

1. **訪問 Node.js 官網**
   - 🌐 https://nodejs.org/

2. **下載 LTS 版本**
   - 選擇 "LTS (Long Term Support)" 版本
   - Windows: 下載 `.msi` 安裝檔
   - 建議版本: Node.js 18.x 或 20.x

3. **安裝 Node.js**
   - 執行下載的安裝檔
   - ✅ 勾選 "Automatically install necessary tools"
   - ✅ 勾選 "Add to PATH"
   - 點擊 "Next" 完成安裝

4. **驗證安裝**
   ```bash
   # 開啟新的命令提示字元視窗
   node --version
   npm --version
   ```

5. **重新執行啟動腳本**
   ```bash
   .\boot-script\START-FULLSTACK.bat
   ```

#### 方法 2: 檢查 PATH 環境變數

如果已安裝 Node.js 但仍顯示找不到 npm：

1. **開啟環境變數設定**
   - Windows 鍵 + R
   - 輸入 `sysdm.cpl` 並按 Enter
   - 點選「進階」→「環境變數」

2. **檢查 PATH**
   - 在「系統變數」中找到 `Path`
   - 確認包含以下路徑：
     ```
     C:\Program Files\nodejs\
     %APPDATA%\npm
     ```

3. **重新啟動命令提示字元**

#### 方法 3: 只啟動後端（暫時解決）

如果暫時不需要前端，可以只啟動後端：

```bash
# 使用只啟動後端的腳本
.\boot-script\START-ALL.bat

# 或
.\boot-script\START-FAST.bat
```

---

## ✅ 修復狀態

### 已修復的問題

1. ✅ **npm 檢查機制**
   - START-FULLSTACK.bat 已加入 npm 檢查
   - START-FULLSTACK-SIMPLE.bat 已加入 npm 檢查
   - 啟動前會提示使用者安裝 Node.js

### 已移除的依賴

1. ✅ **ddgs (DuckDuckGo Search)**
   - 已從 `requirements-api.txt` 移除
   - 已從所有啟動腳本移除相關檢查
   - 改用 OpenAI Responses API 進行網路搜尋

### 預防性改進

- 🛡️ 啟動腳本會在執行前檢查必要工具
- 📝 提供清晰的錯誤訊息和解決方案
- 🔗 直接提供下載連結

---

## 🚀 完整啟動流程

### 首次使用前的準備

#### 1. 安裝 Python（必須）
```
✅ Python 3.11+
下載: https://www.python.org/downloads/
```

#### 2. 安裝 Node.js（只有全棧模式需要）
```
✅ Node.js 18.x 或 20.x LTS
下載: https://nodejs.org/
```

#### 3. 配置 .env 檔案
```bash
# 複製範例檔案
copy .env.example .env

# 編輯 .env，填入必要資訊
notepad .env
```

必須設定的環境變數：
```env
OPENAI_API_KEY=你的OpenAI_API_KEY
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=你的Gmail應用程式密碼
FRONTEND_PATH=C:\路徑\到\前端專案
```

#### 4. 選擇啟動方式

**只啟動後端 API：**
```bash
.\boot-script\START-ALL.bat
```

**啟動前端 + 後端（需要 Node.js）：**
```bash
.\boot-script\START-FULLSTACK.bat
```

---

## 📞 常見問題 FAQ

### Q1: 為什麼需要安裝 Node.js？
**A:** 前端使用 Vite + React 開發，需要 Node.js 環境。如果只使用後端 API，不需要安裝 Node.js。

### Q2: 安裝 Node.js 後仍然找不到 npm？
**A:** 
1. 確認安裝時勾選了 "Add to PATH"
2. 重新啟動命令提示字元視窗
3. 如果還是不行，手動將 Node.js 路徑加入 PATH 環境變數

### Q3: ~~ddgs 模組安裝失敗？~~
**A:** 已不再需要 `ddgs`。專案改用 OpenAI Responses API 進行網路搜尋。

### Q4: 如何驗證所有套件都已安裝？
**A:** 
```bash
# 啟用虛擬環境
.venv\Scripts\activate.bat

# 檢查已安裝的套件
pip list

# 驗證關鍵套件
python -c "import fastapi; print('fastapi OK')"
python -c "import agno; print('agno OK')"
python -c "import openai; print('openai OK')"
```

---

## 📚 相關文檔

- [快速啟動指南](./QUICK_START_NEW_PC.md)
- [啟動說明](./HOW_TO_START.md)
- [UV 遷移說明](./UV_MIGRATION.md)
- [權限問題修復](./PERMISSION_FIX.md)

---

**最後更新**: 2025-11-06  
**狀態**: ✅ 問題已修復並加入預防機制
