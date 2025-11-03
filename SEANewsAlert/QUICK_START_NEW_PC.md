# 🚀 新電腦快速啟動指南

如果您從 GitHub 下載 .zip 解壓縮後遇到問題，請按照此指南操作。

---

## ⚠️ 常見問題：編碼錯誤

### 問題現象
執行 `START-ALL.bat` 時出現亂碼：
```
'銝血???echo' 不是內部或外部命令
'on' 不是內部或外部命令
```

### 原因
GitHub 下載 .zip 時，`.bat` 檔案的編碼可能被破壞。

### 解決方案

#### 方法 1: 使用簡化版啟動腳本（推薦）✅

```bash
# 使用我們提供的無中文版本
.\boot-script\START-SIMPLE.bat
```

#### 方法 2: 手動啟動

```bash
# 1. 安裝依賴（推薦使用 uv，速度更快）
# 安裝 uv（如果未安裝）
pip install uv

# 使用 uv 安裝套件（快 10-100 倍！）
uv pip install -r requirements-api.txt --system

# 或使用傳統 pip
pip install -r requirements-api.txt

# 2. 啟動服務
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 方法 3: 使用 Git Clone（避免編碼問題）

```bash
# 用 git clone 而不是下載 .zip
git clone https://github.com/thisIsCodyLin1201/SEANewsAlert.git
cd SEANewsAlert
.\boot-script\START-ALL.bat
```

---

## 📋 完整啟動步驟（新電腦）

### Windows

```bash
# 1. 解壓縮下載的 .zip
# 2. 進入專案目錄
cd SEANewsAlert

# 3. 創建 .env 檔案
copy .env.example .env

# 4. 編輯 .env（用記事本）
notepad .env
```

**必須填入的資訊**：
```properties
OPENAI_API_KEY=sk-proj-你的真實API_KEY
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=你的Gmail應用程式密碼
```

```bash
# 5. 啟動服務（選擇以下任一方式）

# 方式 A: 使用簡化版腳本（推薦）
.\boot-script\START-SIMPLE.bat

# 方式 B: 手動啟動（使用 uv，更快）
pip install uv
uv pip install -r requirements-api.txt --system
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# 方式 C: 手動啟動（傳統 pip）
pip install -r requirements-api.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### macOS / Linux

```bash
# 1. 解壓縮
# 2. 進入目錄
cd SEANewsAlert

# 3. 創建 .env
cp .env.example .env
nano .env  # 或 vim .env

# 4. 賦予執行權限
chmod +x boot-script/*.sh

# 5. 啟動
./boot-script/START-ALL.sh
```

---

## ✅ 驗證啟動成功

瀏覽器開啟：
- **API 文檔**: http://127.0.0.1:8000/docs
- **健康檢查**: http://127.0.0.1:8000/health

如果看到 API 文檔頁面，表示啟動成功！✅

---

## 🐛 其他常見問題

### Q1: ModuleNotFoundError: No module named 'app'

**原因**：執行目錄不對

**解決**：
```bash
# 確保在專案根目錄（不是 boot-script 目錄）
cd C:\Users\cody9\OneDrive\桌面\SEANewsAlert-main
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Q2: 套件安裝失敗

**解決**：
```bash
# 使用管理員權限
python -m pip install --upgrade pip
python -m pip install -r requirements-api.txt
```

### Q3: 端口被占用

**解決**：
```bash
# 使用其他端口
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

---

## 💡 推薦：使用 Git Clone

為避免編碼和檔案完整性問題，**強烈建議**使用 Git Clone：

```bash
# 1. 安裝 Git (如果還沒有)
# 下載：https://git-scm.com/downloads

# 2. Clone 專案
git clone https://github.com/thisIsCodyLin1201/SEANewsAlert.git

# 3. 進入目錄
cd SEANewsAlert

# 4. 設定 .env
copy .env.example .env
notepad .env

# 5. 啟動
.\boot-script\START-ALL.bat
```

**優點**：
- ✅ 保證檔案完整性
- ✅ 無編碼問題
- ✅ 可以使用 `git pull` 更新
- ✅ 檔案權限正確

---

## 📞 需要幫助？

查看完整文檔：
- [README.md](../README.md)
- [HOW_TO_START.md](../HOW_TO_START.md)
- [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

---

**版本**: 2.0.0 | **更新日期**: 2025-10-23
