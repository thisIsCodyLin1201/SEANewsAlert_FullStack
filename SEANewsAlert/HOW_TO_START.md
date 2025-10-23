# 🚀 啟動指南

## ⚡ 快速啟動

### Windows
```bash
.\boot-script\START-ALL.bat    # 一鍵啟動（推薦）
.\boot-script\START-FAST.bat   # 快速啟動（已安裝）
```

### macOS / Linux
```bash
chmod +x boot-script/*.sh      # 首次執行
./boot-script/START-ALL.sh     # 一鍵啟動
./boot-script/START-FAST.sh    # 快速啟動
```

## 📋 手動啟動

```bash
pip install -r requirements-api.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## 🌐 訪問服務

- **API 文檔**: http://127.0.0.1:8000/docs
- **測試前端**: http://127.0.0.1:8000/static/index.html
- **健康檢查**: http://127.0.0.1:8000/health

## 🐳 Docker 啟動

```bash
docker-compose up -d           # 啟動
docker-compose logs -f         # 查看日誌
docker-compose down            # 停止
```

## ⚙️ 環境配置

1. 複製環境變數：
```bash
cp .env.example .env
```

2. 編輯 `.env` 填入必要資訊：
```env
OPENAI_API_KEY=your_openai_api_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

> ⚠️ **Gmail 使用者**：請使用「應用程式密碼」，不是普通密碼  
> 設定路徑：Google 帳戶 → 安全性 → 兩步驟驗證 → 應用程式密碼

---

## 🔧 故障排除

如果遇到問題，請查看：
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - 完整故障排除指南
- [FRONTEND_API.md](./FRONTEND_API.md) - API 使用文件

---

## 📝 開發模式

啟用自動重載（程式碼變更自動重啟）：

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

**版本**: 2.0.0 | **架構**: FastAPI + RESTful API

## 方法 3: 使用 Python 主程式

### Web 介面

```powershell
python main.py web
```

### 命令列模式

```powershell
python main.py cli -q "搜尋主題" -e "your@email.com"
```

---

## 訪問系統

啟動後，在瀏覽器中訪問：


2. 編輯 `.env`，填入必要資訊：
```bash
OPENAI_API_KEY=your_openai_key
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_app_password  # Gmail 應用程式密碼
```

完整配置說明請查看 `.env.example`

---

**快速提示**: 建議使用 `START-ALL.bat` 一鍵啟動！